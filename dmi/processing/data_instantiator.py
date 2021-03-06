from __future__ import annotations

import abc
import json
from abc import abstractmethod
from typing import List

import pandas

from dmi.fetching import objects


class DMISeries(abc.ABC):
    def __init__(self, description: str, unit: str):
        self.__unit = unit
        self.__description = description

    @property
    def description(self) -> str:
        return self.__description

    @property
    def unit(self) -> str:
        return self.__unit

    @property
    @abstractmethod
    def series(self) -> pandas.Series:
        pass


class DataSeries(DMISeries):
    def __init__(self, data):
        description = data['parameter']
        unit = data['unit']
        values = []
        times = []
        for element in data['dataserie']:
            value = element['value']
            values.append(value)
            raw_time = element['time'] / 1000
            times.append(raw_time)
        index = pandas.to_datetime(times, unit='s', infer_datetime_format=True)
        self.__series = pandas.Series(values, index)
        super().__init__(description, unit)

    @property
    def series(self) -> pandas.Series:
        return self.__series

    def append(self, dmi_series: DMISeries) -> None:
        self.__series = self.series.append(dmi_series.series)


class PredictedSeries(DMISeries):
    def __init__(self, description: str, unit: str):
        super().__init__(description, unit)

    @property
    @abstractmethod
    def forecast(self) -> pandas.Series:
        pass

    @property
    @abstractmethod
    def in_sample_prediction(self) -> pandas.Series:
        pass

    @property
    @abstractmethod
    def prediction_description(self) -> str:
        pass


class LinearRegressionSeries(PredictedSeries):
    def __init__(self, original_dmi_series: DMISeries, full_predicted_series: pandas.Series, prediction_steps: int,
                 linear_regression_description: str):
        super().__init__(original_dmi_series.description, original_dmi_series.unit)
        self.__linear_regression_description = linear_regression_description
        self.__full_predicted_series = full_predicted_series
        self.__prediction_steps = prediction_steps

    @property
    def forecast(self) -> pandas.Series:
        return self.full_predicted_series.iloc[len(self.full_predicted_series) - self.prediction_steps:]

    @property
    def full_predicted_series(self) -> pandas.Series:
        return self.__full_predicted_series

    @property
    def in_sample_prediction(self) -> pandas.Series:
        return self.full_predicted_series.iloc[:-self.prediction_steps]

    @property
    def series(self) -> pandas.Series:
        return self.in_sample_prediction

    @property
    def prediction_steps(self) -> int:
        return self.__prediction_steps

    @property
    def prediction_description(self) -> str:
        return self.__linear_regression_description


class ARIMASeries(PredictedSeries):
    def __init__(self, original_dmi_series: DMISeries, in_sample_prediction: pandas.Series, forecast: pandas.Series,
                 confidence_intervals: pandas.DataFrame, arima_description: str):
        super().__init__(original_dmi_series.description + f'\n{arima_description}', original_dmi_series.unit)
        self.__arima_description = arima_description
        self.__confidence_interval = confidence_intervals
        self.__forecast = forecast
        self.__in_sample_prediction = in_sample_prediction

    @property
    def confidence_intervals(self) -> pandas.DataFrame:
        return self.__confidence_interval

    @property
    def forecast(self) -> pandas.Series:
        return self.__forecast

    @property
    def in_sample_prediction(self) -> pandas.Series:
        return self.__in_sample_prediction

    @property
    def series(self) -> pandas.Series:
        return self.in_sample_prediction

    @property
    def prediction_description(self) -> str:
        return self.__arima_description


class Batch:
    def __init__(self, dmi_series_list: List[DMISeries], area: objects.Area, datatype: objects.DataType,
                 interval: objects.Interval):
        self.__dmi_series_list = dmi_series_list
        self.__area = area
        self.__datatype = datatype
        self.__interval = interval

    @property
    def dmi_series_list(self) -> List[DMISeries]:
        return self.__dmi_series_list

    @property
    def area(self) -> objects.Area:
        return self.__area

    @property
    def datatype(self) -> objects.DataType:
        return self.__datatype

    @property
    def interval(self):
        return self.__interval

    def to_dataframe(self):
        series_list = [x.series for x in self.__dmi_series_list]
        return pandas.concat(series_list, axis=1)


class DataBatch(Batch):
    def __init__(self, data, area: objects.Area, datatype: objects.DataType, interval: objects.Interval):
        series_list = []
        for element in data:
            data_series = DataSeries(element)
            series_list.append(data_series)
        super().__init__(series_list, area, datatype, interval)

    # noinspection PyTypeChecker
    @property
    def data_series_list(self) -> List[DataSeries]:
        return self.dmi_series_list

    def append(self, data_batch: DataBatch):
        for i in range(len(self.dmi_series_list)):
            self.data_series_list[i].append(data_batch.dmi_series_list[i])


class PredictedBatch(Batch):
    def __init__(self, original_data_batch: Batch, predicted_series: List[PredictedSeries]):
        super().__init__(predicted_series, original_data_batch.area, original_data_batch.datatype,
                         original_data_batch.interval)

    # noinspection PyTypeChecker
    @property
    def predicted_series_list(self) -> List[PredictedSeries]:
        return self.dmi_series_list


def __convert(data: str):
    converted_data = json.loads(data)
    if not isinstance(converted_data, list):
        converted_data = [converted_data]
    return converted_data


def instantiate_data(data: str, area: objects.Area, datatype: objects.DataType, interval: objects.Interval):
    converted_data = __convert(data)
    return DataBatch(converted_data, area, datatype, interval)
