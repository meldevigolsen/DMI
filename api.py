from dmi.fetching import objects, downloader
from dmi.processing import data_instantiator
import datetime


def get_hourly_databatch(area: objects.Area, datatype: objects.DataType, date: datetime.datetime):
    data = downloader.get_hourly_data(
        area, datatype, date.year, date.month, date.day)
    databatch = data_instantiator.instantiate_data(data, area, datatype)
    return databatch


def get_daily_databatch(area: objects.Area, datatype: objects.DataType, date: datetime.datetime):
    data = downloader.get_daily_data(area, datatype, date.year, date.month)
    databatch = data_instantiator.instantiate_data(data, area, datatype)
    return databatch


def get_monthly_databatch(area: objects.Area, datatype: objects.DataType, year: int):
    data = downloader.get_monthly_data(area, datatype, year)
    databatch = data_instantiator.instantiate_data(data, area, datatype)
    return databatch


def get_yearly_databatch(area: objects.Area, datatype: objects.DataType, start_year: int, end_year: int):
    data = downloader.get_yearly_data(area, datatype, start_year, end_year)
    databatch = data_instantiator.instantiate_data(data, area, datatype)
    return databatch


def get_hourly_databulk(area: objects.Area, datatype: objects.DataType, start_date: datetime.datetime, end_date: datetime.datetime):
    delta = (end_date - start_date).days
    dates = [start_date + datetime.timedelta(days=x) for x in range(delta + 1)]
    data_list = []
    for date in dates:
        data_list.append(get_hourly_databatch(area, datatype, date))
    databulk = data_instantiator.instantiate_bulk_data(
        data_list, area, datatype)
    return databulk


def get_daily_databulk(area: objects.Area, datatype: objects.DataType, start_date: datetime.datetime, end_date: datetime.datetime):
    delta = (end_date - start_date).months
    dates = [start_date + datetime.timedelta(months=x)
             for x in range(delta + 1)]
    data_list = []
    for date in dates:
        data_list.append(get_daily_databatch(area, datatype, date))
    databulk = data_instantiator.instantiate_bulk_data(
        data_list, area, datatype)
    return databulk


def get_monthly_databulk(area: objects.Area, datatype: objects.DataType, start_year: int, end_year: int):
    data_list = []
    for year in range(start_year, end_year + 1):
        data_list.append(get_monthly_databatch(area, datatype, year))
    databulk = data_instantiator.instantiate_bulk_data(
        data_list, area, datatype)
    return databulk
