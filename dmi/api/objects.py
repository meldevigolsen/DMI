from __future__ import annotations
from enum import Enum
import json

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


COUNTRIES = [Country('danmark'),
             Country('grønland'),
             Country('færøerne')]


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

class DataType(Enum):
    PRECIPITATION = "precip",
    PRESSURE = "pressure",
    HUMIDITY = "humidity",
    SUN_HOURS = "sunhours",
    DROUGHT = "drought",
    LIGHTNING = "lightning",
    SNOW = "snow",
    TEMPERATURE = "temperature",
    WIND = "wind",
    WIND_DIRECTION = "winddir",


def __load_areas_json(filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def __insert_all_areas():
    for country in COUNTRIES:
        area_names = __load_areas_json(f'dmi/{country.name}.json')
        for area_name in area_names:
            area = Area(area_name, country)
            country.add_area(area)

__insert_all_areas