import downloader
import objects
import datetime


def get_bulk_hourly_data(area: objects.Area, datatype: objects.DataType, start_date: datetime.datetime, end_date: datetime.datetime):
    delta = (end_date - start_date).days
    dates = [start_date + datetime.timedelta(days=x) for x in range(delta + 1)]
    data_list = []
    for date in dates:
        data_list.append(downloader.get_hourly_data(
            area, datatype, date.year, date.month, date.day))
    return data_list


def get_bulk_daily_data(area: objects.Area, datatype: objects.DataType, start_date: datetime.datetime, end_date: datetime.datetime):
    delta = (end_date - start_date).months
    dates = [start_date + datetime.timedelta(months=x)
             for x in range(delta + 1)]
    data_list = []
    for date in dates:
        data_list.append(downloader.get_daily_data(
            area, datatype, date.year, date.month))
    return data_list


def get_bulk_monthly_data(area: objects.Area, datatype: objects.DataType, start_year: int, end_year: int):
    data_list = []
    for year in range(start_year, end_year + 1):
        data_list.append(downloader.get_monthly_data(area, datatype, year))
    return data_list
