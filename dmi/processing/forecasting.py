import numpy
import pandas
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

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
    prediction_series = data_instantiator.PredictedSeries(dmi_series, prediction)
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
        batch, predicted_series_list)
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
    predicted_batch = data_instantiator.PredictedBatch(batch, predict_series_list)
    return predicted_batch
