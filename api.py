from dmi.fetching import objects, downloader
from dmi.processing import data_instantiator
import datetime


def get_data_batch(area: objects.Area, datatype: objects.DataType, interval: objects.Interval, date: datetime.datetime):
    data = downloader.get_data(area, datatype, interval, date)
    data_batch = data_instantiator.instantiate_data(data, area, datatype)
    return data_batch


def get_yearly_data_batch(area: objects.Area, datatype: objects.DataType, start_year: int, end_year: int):
    data = downloader.get_yearly_data(area, datatype, start_year, end_year)
    data_batch = data_instantiator.instantiate_data(data, area, datatype)
    return data_batch


def get_data_timespan(area: objects.Area, datatype: objects.DataType, interval: objects.Interval, start_date: datetime.datetime, end_date: datetime.datetime):
    dates = []
    if interval == objects.Interval.HOURLY:
        delta = (end_date - start_date).days
        dates = [start_date +
                 datetime.timedelta(days=x) for x in range(delta + 1)]
    elif interval == objects.Interval.DAILY:
        delta = (end_date - start_date).months
        dates = [start_date +
                 datetime.timedelta(months=x) for x in range(delta + 1)]
    elif interval == objects.Interval.MONTHLY:
        delta = (end_date - start_date).years
        dates = [start_date +
                 datetime.timedelta(years=x) for x in range(delta + 1)]
    data_list = []
    for date in dates:
        data_list.append(get_data_batch(area, datatype, interval, date))
    data_timespan = data_instantiator.instantiate_data_timespan(
        data_list, area, datatype)
    return data_timespan

