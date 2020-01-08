from __future__ import annotations
import json
import datetime
import pandas
from dmi.fetching import objects
from typing import List


class DMISeries:
    def __init__(self, description: str, unit: str, series: pandas.Series):
        self.__description = description
        self.__unit = unit
        self.__series = series

    @property
    def description(self) -> str:
        return self.__description

    @property
    def unit(self) -> str:
        return self.__unit

    @property
    def series(self) -> pandas.Series:
        return self.__series

    def append(self, dmi_series: DMISeries):
        self.series.append(dmi_series.series)


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
        index = pandas.to_datetime(times, unit='s')
        series = pandas.Series(values, index)
        super().__init__(description, unit, series)


class PredictedSeries(DMISeries):
    def __init__(self, original_dmi_series: DMISeries, series: pandas.Series):
        super().__init__(original_dmi_series.description + ' (prediction)',
                         original_dmi_series.unit, series)


class Batch:
    def __init__(self, dmi_series_list: List[DMISeries], area: objects.Area, datatype: objects.DataType):
        self.__dmi_series_list = dmi_series_list
        self.__area = area
        self.__datatype = datatype

    @property
    def dmi_series_list(self) -> List[DMISeries]:
        return self.__dmi_series_list

    @property
    def area(self) -> objects.Area:
        return self.__area

    @property
    def datatype(self) -> objects.DataType:
        return self.__datatype

    def to_dataframe(self):
        series_list = [x.series for x in self.__dmi_series_list]
        return pandas.concat(series_list, axis=1)


class DataBatch(Batch):
    def __init__(self, data, area: objects.Area, datatype: objects.DataType, is_prediction=False):
        series_list = []
        for element in data:
            data_series = DataSeries(element)
            series_list.append(data_series)
        super().__init__(series_list, area, datatype)

    def append(self, data_batch: DataBatch):
        for i in range(len(self.dmi_series_list)):
            self.dmi_series_list[i].append(data_batch.dmi_series_list[i])


class PredictedBatch(Batch):
    def __init__(self, original_data_batch: DataBatch, predicted_series: List[PredictedSeries]):
        super().__init__(predicted_series, original_data_batch.area, original_data_batch.datatype)


def __convert(data: str):
    converted_data = json.loads(data)
    if not isinstance(converted_data, list):
        converted_data = [converted_data]
    return converted_data


def instantiate_data(data: str, area: objects.Area, datatype: objects.DataType):
    converted_data = __convert(data)
    return DataBatch(converted_data, area, datatype)
