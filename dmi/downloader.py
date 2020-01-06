import objects
import url_generator
import requests


def __parse_data(raw_data):
    return raw_data.decode('utf-8')


def __get_data(url: str):
    response = requests.get(url)
    raw_data = response.content
    return __parse_data(raw_data)


def get_hourly_data(area: objects.Area, datatype: objects.DataType, year: int, month: int, day: int):
    url = url_generator.generate_hourly_url(area, datatype, year, month, day)
    return __get_data(url)


def get_daily_data(area: objects.Area, datatype: objects.DataType, year: int, month: int):
    url = url_generator.generate_daily_url(area, datatype, year, month)
    return __get_data(url)


def get_monthly_data(area: objects.Area, datatype: objects.DataType, year: int):
    url = url_generator.generate_monthly_url(area, datatype, year)
    return __get_data(url)


def get_yearly_data(area: objects.Area, datatype: objects.DataType, start_year: int, end_year: int):
    url = url_generator.generate_yearly_url(
        area, datatype, start_year, end_year)
    return __get_data(url)
