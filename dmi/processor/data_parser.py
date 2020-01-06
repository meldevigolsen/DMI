import json
import datetime
import pandas
from dmi.api import objects


class DataPoint:
    def __init__(self, value: float, timestamp: int):
        self.__value = value
        self.__datetime = datetime.datetime.fromtimestamp(
            timestamp / float(1000))

    @property
    def value(self):
        return self.__value

    @property
    def datetime(self):
        return self.__datetime


class DataSeries:
    def __init__(self, data):
        self.__description = data['parameter']
        self.__unit = data['unit']
        self.__datapoints = []
        for element in data['dataserie']:
            raw_time = element['time']
            value = element['value']
            data_point = DataPoint(value, raw_time)
            self.__datapoints.append(data_point)

    @property
    def desciption(self):
        return self.__description

    @property
    def unit(self):
        return self.__unit

    @property
    def datapoints(self):
        return self.__datapoints

    @property
    def values(self):
        return [datapoint.value for datapoint in self.datapoints]

    @property
    def datetimes(self):
        return [datapoint.datetime for datapoint in self.datapoints]

    def to_pandas_series(self):
        index = pandas.DatetimeIndex(self.datetimes)
        series = pandas.Series(self.values, index)
        return series


class DataBatch:
    def __init__(self, data, area: objects.Area, datatype: objects.DataType):
        self.__data_series = []
        self.__area = area
        self.__datatype = datatype
        for element in data:
            data_series = DataSeries(element)
            self.__data_series.append(data_series)

    @property
    def data_series(self):
        return self.__data_series

    @property
    def area(self):
        return self.__area

    @property
    def datatype(self):
        return self.__datatype

    def to_pandas_dataframe(self):
        return pandas.concat([series.to_pandas_series() for series in self.data_series], axis=1)


def __convert(data: str):
    converted_data = json.loads(data)
    if not isinstance(converted_data, list):
        converted_data = [converted_data]
    return converted_data


def instantiate_data(data: str, area: objects.Area, datatype: objects.DataType):
    converted_data = __convert(data)
    return DataBatch(converted_data, area, datatype)
