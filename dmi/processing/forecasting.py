import numpy
import pandas
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
from statsmodels.tsa.statespace.mlemodel import PredictionResults
from statsmodels.tsa.statespace.sarimax import SARIMAX, SARIMAXResults
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
        diff_data = series.diff(diff_order) if diff_order > 0 else series
        acf_res, conf_int = acf(diff_data.values, alpha=.05)
        confidence_interval = __confidence_interval_calculator(acf_res, conf_int)
        spike_counter = 0
        for i in range(1, spike_limit + 1):
            if acf_res[i] > confidence_interval[1][i]:
                spike_counter += 1
        if spike_counter < spike_limit:
            best_diff_order = diff_order
            break
    return best_diff_order


def __find_best_ar_order(series: pandas.Series, diff_order):
    diff_data = series.diff(diff_order) if diff_order > 0 else series
    pacf_res, confint = pacf(diff_data.values, alpha=.05)
    confidence_interval = __confidence_interval_calculator(pacf_res, confint)
    spike_counter = 0
    for i in range(1, 5):
        if pacf_res[i] > confidence_interval[1][i]:
            spike_counter += 1
    return spike_counter


def __find_best_ma_order_arima(resid):
    acf_res, confint = acf(resid, alpha=.05)
    confidence_interval = __confidence_interval_calculator(acf_res, confint)
    spike_counter = 0
    for i in range(1, 5):
        if acf_res[i] < confidence_interval[0][i]:
            spike_counter += 1
    return spike_counter


def __arima_prediction(data_series: data_instantiator.DataSeries, steps: int):
    series = data_series.series
    diff_order = __find_best_differencing_order_arima(series)
    ar_order = __find_best_ar_order(series, diff_order)
    resid = ARIMA(series, (ar_order, diff_order, 0)).fit(disp=0).resid
    ma_order = __find_best_ma_order_arima(resid)
    order = (ar_order, diff_order, ma_order)
    model_fit: ARIMAResults = ARIMA(series, order).fit(disp=0)
    result: pandas.Series = model_fit.predict(end=series.index[-1])
    forecast, stderr, conf_int = model_fit.forecast(steps)
    freq = series.index.inferred_freq
    index = pandas.date_range(series.index[-1] + pandas.to_timedelta(1, freq), periods=steps, freq=freq)
    forecast_series = pandas.Series(forecast, index)
    confidence_intervals = pandas.DataFrame(conf_int, index, ['lower_limit', 'upper_limit'])
    predicted_series = data_instantiator.ARIMASeries(data_series, result, forecast_series, confidence_intervals,
                                                     f'ARIMA{order}')
    return predicted_series


def arima_prediction(data_batch: data_instantiator.DataBatch, steps: int):
    predicted_series_list = []
    for dmi_series in data_batch.data_series_list:
        predicted_series_list.append(__arima_prediction(dmi_series, steps))
    predicted_batch = data_instantiator.PredictedBatch(data_batch, predicted_series_list)
    return predicted_batch


def __sarimax_prediction(data_series: data_instantiator.DataSeries, seasonal_steps: int, steps: int):
    default_seasonal_order = (0, 1, 0, seasonal_steps)
    series = data_series.series
    diff_order = __find_best_differencing_order_arima(series)
    ar_order = __find_best_ar_order(series, diff_order)
    resid = SARIMAX(series, order=(ar_order, diff_order, 0), seasonal_order=default_seasonal_order).fit(disp=0).resid
    ma_order = __find_best_ma_order_arima(resid)
    order = (ar_order, diff_order, ma_order)
    temp_model_fit = SARIMAX(series, order=order, seasonal_order=default_seasonal_order).fit(disp=0)
    acf_res, acf_confint = acf(temp_model_fit.resid, alpha=.05)
    acf_confint = __confidence_interval_calculator(acf_res, acf_confint)
    seasonal_order = default_seasonal_order
    if acf_res[seasonal_steps] < acf_confint[0][seasonal_steps]:
        seasonal_order = (0, 1, 1, seasonal_steps)
    elif acf_res[seasonal_steps] > acf_confint[1][seasonal_steps]:
        seasonal_order = (1, 1, 0, seasonal_steps)
    # noinspection PyTypeChecker
    model_fit: SARIMAXResults = SARIMAX(series, order=order, seasonal_order=seasonal_order).fit(disp=0)
    # noinspection PyTypeChecker
    result: pandas.Series = model_fit.predict(end=series.index[-1])
    # noinspection PyTypeChecker
    forecast: PredictionResults = model_fit.get_forecast(steps)
    forecast_series: pandas.Series = forecast.predicted_mean
    confidence_intervals: pandas.DataFrame = forecast.conf_int()
    confidence_intervals.columns = ['lower_limit', 'upper_limit']
    predicted_series = data_instantiator.ARIMASeries(data_series, result, forecast_series, confidence_intervals,
                                                     f'SARIMAX{order}x{seasonal_order}')
    return predicted_series


def sarimax_prediction(data_batch: data_instantiator.DataBatch, seasonal_steps: int, steps: int):
    predicted_series_list = []
    for dmi_series in data_batch.data_series_list:
        predicted_series_list.append(__sarimax_prediction(dmi_series, seasonal_steps, steps))
    predicted_batch = data_instantiator.PredictedBatch(data_batch, predicted_series_list)
    return predicted_batch
