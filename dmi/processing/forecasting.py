import numpy
import pandas
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import acf, pacf

from dmi.processing import data_instantiator


def __x_generator(steps: int):
    return numpy.array([x for x in range(steps)]).reshape(-1, 1)


def __extend_date_index(index: pandas.DatetimeIndex, steps: int) -> pandas.DatetimeIndex:
    extension = pandas.date_range(
        index[-1], periods=steps + 1, freq=index.inferred_freq)
    return index.union(extension)


def __prediction_converter(dmi_series: data_instantiator.DMISeries, linreg: LinearRegression, x: numpy.ndarray,
                           steps: int, description: str):
    prediction_values = linreg.predict(x)
    index = dmi_series.series.index
    if steps > 0:
        index = __extend_date_index(index, steps)
    prediction = pandas.Series(prediction_values, index)
    prediction_series = data_instantiator.LinearRegressionSeries(dmi_series, prediction, steps, description)
    return prediction_series


def __linear_regression(dmi_series: data_instantiator.DMISeries, steps=0) -> data_instantiator.LinearRegressionSeries:
    linreg = LinearRegression()
    series = dmi_series.series
    x = __x_generator(len(series))
    linreg.fit(x, series.values)
    mse = mean_squared_error(series.values, linreg.predict(x))
    x = __x_generator(len(series) + steps)
    description = f'linreg mse:~{round(mse, 2)}'
    prediction_series = __prediction_converter(dmi_series, linreg, x, steps, description)
    return prediction_series


def linear_regression(batch: data_instantiator.Batch, steps=0) -> data_instantiator.PredictedBatch:
    predicted_series_list = []
    for dmi_series in batch.dmi_series_list:
        predicted_series_list.append(__linear_regression(dmi_series, steps))
    predicted_batch = data_instantiator.PredictedBatch(batch, predicted_series_list)
    return predicted_batch


def __polynomial_linear_regression(dmi_series: data_instantiator.DMISeries, poly_feat: PolynomialFeatures, steps=0):
    linreg = LinearRegression()
    series = dmi_series.series
    x = poly_feat.fit_transform(__x_generator(len(series)))
    linreg.fit(x, series.values)
    mse = mean_squared_error(series.values, linreg.predict(x))
    description = f'polylinreg d:{poly_feat.degree} mse:~{round(mse, 2)}'
    x = poly_feat.fit_transform(__x_generator(len(series) + steps))
    prediction_series = __prediction_converter(dmi_series, linreg, x, steps, description)
    return prediction_series


def polynomial_linear_regression(batch: data_instantiator.Batch, degree: int, steps=0):
    poly_feat = PolynomialFeatures(degree)
    predict_series_list = []
    for dmi_series in batch.dmi_series_list:
        predict_series_list.append(__polynomial_linear_regression(dmi_series, poly_feat, steps))
    predicted_batch = data_instantiator.PredictedBatch(batch, predict_series_list)
    return predicted_batch


def __confidence_interval_calculator(res: numpy.ndarray, confint: numpy.ndarray):
    return numpy.array([confint[:, 0] - res, confint[:, 1] - res])


def __find_best_differencing_order_arima(series: pandas.Series):
    spike_limit = 10
    best_diff_order = 0
    for diff_order in range(3):
        model = ARIMA(series.values, (0, diff_order, 0))
        model_fit: ARIMAResults = model.fit(disp=0)
        acf_res, conf_int = acf(model_fit.resid, alpha=.05, nlags=25)
        confidence_interval = __confidence_interval_calculator(acf_res, conf_int)
        spike_counter = 0
        for i in range(1, spike_limit + 1):
            if acf_res[i] > confidence_interval[1][i]:
                spike_counter += 1
        if spike_counter < spike_limit:
            best_diff_order = diff_order
            break
    return best_diff_order


def __find_best_ar_order_arima(series: pandas.Series, diff_order):
    model = ARIMA(series, (0, diff_order, 0))
    model_fit: ARIMAResults = model.fit(disp=0)
    pacf_res, confint = pacf(model_fit.resid, alpha=.05)
    confidence_interval = __confidence_interval_calculator(pacf_res, confint)
    spike_counter = 0
    for i in range(1, 5):
        if pacf_res[i] > confidence_interval[1][i]:
            spike_counter += 1
    return spike_counter


def __find_best_ma_order_arima(series: pandas.Series, diff_order, ar_order):
    model = ARIMA(series.values, (ar_order, diff_order, 0))
    model_fit: ARIMAResults = model.fit(disp=0)
    acf_res, confint = acf(model_fit.resid, alpha=.05)
    confidence_interval = __confidence_interval_calculator(acf_res, confint)
    spike_counter = 0
    for i in range(1, 5):
        if acf_res[i] < confidence_interval[0][i]:
            spike_counter += 1
    return spike_counter


def __arima_prediction(data_series: data_instantiator.DataSeries, steps):
    series = data_series.series
    diff_order = __find_best_differencing_order_arima(series)
    ar_order = __find_best_ar_order_arima(series, diff_order)
    ma_order = __find_best_ma_order_arima(series, diff_order, ar_order)
    order = (ar_order, diff_order, ma_order)
    model = ARIMA(series, order)
    model_fit: ARIMAResults = model.fit(disp=0)
    prediction_end = series.index[-1]
    result: pandas.Series = model_fit.predict(end=prediction_end)
    forecast, stderr, conf_int = model_fit.forecast(steps)
    freq = series.index.inferred_freq
    index = pandas.date_range(series.index[-1] + pandas.to_timedelta(1, freq), periods=steps, freq=freq)
    forecast_series = pandas.Series(forecast, index)
    confidence_intervals = pandas.DataFrame(conf_int, index, ['lower_limit', 'upper_limit'])
    predicted_series = data_instantiator.ARIMASeries(data_series, result, forecast_series, confidence_intervals,
                                                     f'ARIMA({order})')
    return predicted_series


def arima_prediction(data_batch: data_instantiator.DataBatch, steps):
    predicted_series_list = []
    for dmi_series in data_batch.data_series_list:
        predicted_series_list.append(__arima_prediction(dmi_series, steps))
    predicted_batch = data_instantiator.PredictedBatch(data_batch, predicted_series_list)
    return predicted_batch


def __find_best_ar_order_sarimax(series: pandas.Series, seasonal_steps: int):
    for diff_order in range(3):
        model = SARIMAX(series, order=(0, diff_order, 0), seasonal_order=(0, 1, 0, seasonal_steps))
        model_fit = model.fit(disp=0)


def __sarimax_prediction(dmi_series: data_instantiator.DMISeries, seasonal_steps: int, steps: int):
    series = dmi_series.series
    s_diff_order = 1
