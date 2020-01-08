from sklearn.linear_model import LinearRegression
import pandas
import numpy
from dmi.processing import data_instantiator


def __x_generator(steps: int):
    return numpy.array([x for x in range(steps)]).reshape(-1, 1)


def __extend_date_index(index: pandas.DatetimeIndex, steps: int) -> pandas.DatetimeIndex:
    extension = pandas.date_range(
        index[-1], periods=steps+1, freq=index.freqstr)
    return index.union(extension)


def __linear_regression(dmi_series: data_instantiator.DMISeries, steps=0) -> data_instantiator.PredictedSeries:
    linreg = LinearRegression()
    series = dmi_series.series
    x = __x_generator(len(series))
    linreg.fit(x, series.values)
    if steps > 0:
        x = __x_generator(len(series) + steps)
    prediction_values = linreg.predict(x)
    prediction = pandas.Series(prediction_values, series.index)
    predicted_series = data_instantiator.PredictedSeries(
        dmi_series, prediction)
    return predicted_series


def linear_regression(batch: data_instantiator.Batch, steps=0) -> data_instantiator.PredictedBatch:
    predicted_series_list = []
    for dmi_series in batch.dmi_series_list:
        predicted_series_list.append(__linear_regression(dmi_series, steps))
    prediction_batch = data_instantiator.PredictedBatch(
        batch, predicted_series_list)
    return prediction_batch
