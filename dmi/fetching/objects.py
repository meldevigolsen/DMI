from __future__ import annotations

import json
from enum import Enum

months = {
    1: 'Januar',
    2: 'Februar',
    3: 'Marts',
    4: 'April',
    5: 'Maj',
    6: 'Juni',
    7: 'Juli',
    8: 'August',
    9: 'September',
    10: 'Oktober',
    11: 'November',
    12: 'December'
}


class Interval:
    def __init__(self, url_name: str, danish_name: str, freq: str):
        self.__url_name = url_name
        self.__danish_name = danish_name
        self.__freq = freq

    @property
    def url_name(self):
        return self.__url_name

    @property
    def danish_name(self):
        return self.__danish_name

    @property
    def freq(self):
        return self.__freq


class Intervals(Enum):
    HOURLY = Interval('hourly', 'Timer', 'H')
    DAILY = Interval('daily', 'Dage', 'D')
    MONTHLY = Interval('monthly', 'Måneder', 'MS')
    YEARLY = Interval('yearly', 'År', 'AS')


class Country:
    def __init__(self, name: str):
        self.__name = name
        self.__areas = []

    @property
    def name(self):
        return self.__name

    @property
    def fine_name(self):
        return self.name[0].upper() + self.name[1:]

    @property
    def areas(self):
        return self.__areas

    def add_area(self, area: Area):
        self.__areas.append(area)


class Countries(Enum):
    DENMARK = Country('danmark')
    GREENLAND = Country('grønland')
    FAROE_ISLANDS = Country('færøerne')

    # noinspection PyTypeChecker
    @staticmethod
    def list_items():
        return [item.value for item in list(Countries)]


class Area:
    def __init__(self, name: str, country: Country):
        self.__name = name
        self.__country = country

    @property
    def name(self):
        return self.__name

    @property
    def country(self):
        return self.__country


class DataType:
    def __init__(self, url_name: str, full_name: str, danish_name: str):
        self.__url_name = url_name
        self.__full_name = full_name
        self.__danish_name = danish_name

    @property
    def url_name(self):
        return self.__url_name

    @property
    def full_name(self):
        return self.__full_name

    @property
    def danish_name(self):
        return self.__danish_name


class DataTypes(Enum):
    PRECIPITATION = DataType("precip", 'Precipitation', 'Nedbør')
    PRESSURE = DataType("pressure", 'Pressure', 'Lufttryk')
    HUMIDITY = DataType("humidity", 'Humidity', 'Luftfugtighed')
    SUN_HOURS = DataType("sunhours", 'Sun hours', 'Soltimer')
    DROUGHT = DataType("drought", 'Drought', 'Tørke')
    LIGHTNING = DataType("lightning", 'Lightning', 'Lynnedslag')
    SNOW = DataType("snow", 'Snow', 'Sne')
    TEMPERATURE = DataType("temperature", 'Temperature', 'Temperatur')
    WIND = DataType("wind", 'Wind', 'Vind')
    WIND_DIRECTION = DataType("winddir", 'Wind direction', 'Vindretning')


def __load_areas_json(filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def __insert_all_areas():
    for country in Countries.list_items():
        if len(country.areas) == 0:
            area_names = __load_areas_json(
                f'C:/Users/Martin/PycharmProjects/DMI/dmi/fetching/data/{country.name}.json')
            for area_name in area_names:
                area = Area(area_name, country)
                country.add_area(area)


__insert_all_areas()
