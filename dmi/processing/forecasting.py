import numpy
import pandas
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
from statsmodels.tsa.stattools import acf, pacf, adfuller

from dmi.processing import data_instantiator


def __x_generator(steps: int):
    return numpy.array([x for x in range(steps)]).reshape(-1, 1)


def __extend_date_index(index: pandas.DatetimeIndex, steps: int) -> pandas.DatetimeIndex:
    extension = pandas.date_range(
        index[-1], periods=steps + 1, freq=index.inferred_freq)
    return index.union(extension)


def __prediction_converter(dmi_series: data_instantiator.DMISeries, linreg: LinearRegression, x: numpy.ndarray,
                           steps: int):
    prediction_values = linreg.predict(x)
    index = dmi_series.series.index
    if steps > 0:
        index = __extend_date_index(index, steps)
    prediction = pandas.Series(prediction_values, index)
    prediction_series = data_instantiator.PredictedSeries(dmi_series, prediction, steps)
    return prediction_series


def __linear_regression(dmi_series: data_instantiator.DMISeries, steps=0) -> data_instantiator.PredictedSeries:
    linreg = LinearRegression()
    series = dmi_series.series
    x = __x_generator(len(series))
    linreg.fit(x, series.values)
    x = __x_generator(len(series) + steps)
    prediction_series = __prediction_converter(dmi_series, linreg, x, steps)
    return prediction_series


def linear_regression(batch: data_instantiator.Batch, steps=0) -> data_instantiator.PredictedBatch:
    predicted_series_list = []
    for dmi_series in batch.dmi_series_list:
        predicted_series_list.append(__linear_regression(dmi_series, steps))
    predicted_batch = data_instantiator.PredictedBatch(
        batch, predicted_series_list, steps)
    return predicted_batch


def __polynomial_linear_regression(dmi_series: data_instantiator.DMISeries, poly_feat: PolynomialFeatures, steps=0):
    linreg = LinearRegression()
    series = dmi_series.series
    x = poly_feat.fit_transform(__x_generator(len(series)))
    linreg.fit(x, series.values)
    x = poly_feat.fit_transform(__x_generator(len(series) + steps))
    prediction_series = __prediction_converter(dmi_series, linreg, x, steps)
    return prediction_series


def polynomial_linear_regression(batch: data_instantiator.Batch, degree: int, steps=0):
    poly_feat = PolynomialFeatures(degree)
    predict_series_list = []
    for dmi_series in batch.dmi_series_list:
        predict_series_list.append(__polynomial_linear_regression(dmi_series, poly_feat, steps))
    predicted_batch = data_instantiator.PredictedBatch(batch, predict_series_list, steps)
    return predicted_batch


def __find_best_differencing_order(series: pandas.Series):
    diff_series = series
    diff_order = 0
    for i in range(3):
        # noinspection PyTypeChecker
        adf: tuple = adfuller(diff_series)
        if adf[1] < .5:
            diff_order = i
            break
        else:
            diff_series = diff_series.diff()
            diff_order += 1
    return diff_order


def __find_best_ar_order(series: pandas.Series, diff_order):
    model = ARIMA(series, (0, diff_order, 0))
    model_fit: ARIMAResults = model.fit(disp=0)
    pacf_res, confidence_level = pacf(model_fit.resid, alpha=.05)
    spike_counter = 0
    for i in range(1, 5):
        if pacf_res[i] > confidence_level[i][1]:
            spike_counter += 1
    return spike_counter


def __find_best_ma_order(series: pandas.Series, diff_order):
    model = ARIMA(series.values, (0, diff_order, 0))
    model_fit: ARIMAResults = model.fit(disp=0)
    acf_res, confidence_level = acf(model_fit.resid, alpha=.05)
    spike_counter = 0
    for i in range(1, 5):
        if acf_res[i] < confidence_level[i][0]:
            spike_counter += 1
    return spike_counter


def __arima_prediction(dmi_series: data_instantiator.DMISeries, steps):
    series = dmi_series.series
    diff_order = __find_best_differencing_order(series)
    ar_order = __find_best_ar_order(series, diff_order)
    ma_order = __find_best_ma_order(series, diff_order)
    model = ARIMA(series, (ar_order, diff_order, ma_order))
    model_fit: ARIMAResults = model.fit(disp=0)
    prediction_end = series.index[-1]
    if steps > 0:
        prediction_end = prediction_end + pandas.to_timedelta(steps, unit=series.index.inferred_freq)
    result = model_fit.predict(start=series.index[diff_order], end=prediction_end)
    predicted_series = data_instantiator.PredictedSeries(dmi_series, result, steps)
    return predicted_series


def arima_prediction(batch: data_instantiator.Batch, steps=0):
    predicted_series_list = []
    for dmi_series in batch.dmi_series_list:
        predicted_series_list.append(__arima_prediction(dmi_series, steps))
    predicted_batch = data_instantiator.PredictedBatch(batch, predicted_series_list, steps)
    return predicted_batch
