from dmi.fetching import objects, url_generator
import requests
import datetime


def __parse_data(raw_data):
    return raw_data.decode('utf-8')


def __get_data(url: str):
    response = requests.get(url)
    raw_data = response.content
    return __parse_data(raw_data)


def get_data(area: objects.Area, datatype: objects.DataType, interval: objects.Interval, date: datetime.datetime):
    if interval == objects.Interval.HOURLY:
        url = url_generator.generate_hourly_url(
            area, datatype, date.year, date.month, date.day)
    elif interval == objects.Interval.DAILY:
        url = url_generator.generate_daily_url(
            area, datatype, date.year, date.month)
    elif interval == objects.Interval.MONTHLY:
        url = url_generator.generate_monthly_url(area, datatype, date.year)
    return __get_data(url)


def get_yearly_data(area: objects.Area, datatype: objects.DataType, start_year: int, end_year: int):
    url = url_generator.generate_yearly_url(
        area, datatype, start_year, end_year)
    return __get_data(url)
