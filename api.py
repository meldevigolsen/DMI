import datetime
from typing import Optional

from dmi.fetching import objects, downloader
from dmi.processing import data_instantiator


def get_data_batch(area: objects.Area, datatypes: objects.DataTypes, intervals: objects.Intervals,
                   date: datetime.datetime) -> data_instantiator.DataBatch:
    interval = intervals.value
    datatype = datatypes.value
    data = downloader.get_data(area, datatype, interval, date)
    data_batch = data_instantiator.instantiate_data(data, area, datatype, interval)
    return data_batch


def get_yearly_data_batch(area: objects.Area, datatypes: objects.DataTypes, start_year: int,
                          end_year: int) -> data_instantiator.DataBatch:
    datatype = datatypes.value
    data = downloader.get_yearly_data(area, datatype, start_year, end_year)
    data_batch = data_instantiator.instantiate_data(data, area, datatype, objects.Intervals.YEARLY.value)
    return data_batch


def get_data_timespan(area: objects.Area, datatype: objects.DataTypes, intervals: objects.Intervals,
                      start_date: datetime.datetime, end_date: datetime.datetime) -> data_instantiator.DataBatch:
    dates = []
    if intervals == objects.Intervals.HOURLY:
        delta = (end_date - start_date).days
        dates = [start_date +
                 datetime.timedelta(days=x) for x in range(delta + 1)]
    elif intervals == objects.Intervals.DAILY:
        delta = (end_date - start_date).months
        # noinspection PyArgumentList
        dates = [start_date + datetime.timedelta(months=x) for x in range(delta + 1)]
    elif intervals == objects.Intervals.MONTHLY:
        delta = (end_date - start_date).years
        # noinspection PyArgumentList
        dates = [start_date +
                 datetime.timedelta(years=x) for x in range(delta + 1)]
    first_batch: Optional[data_instantiator.DataBatch] = None
    for date in dates:
        data_batch = get_data_batch(area, datatype, intervals, date)
        if first_batch is None:
            first_batch = data_batch
        else:
            first_batch.append(data_batch)
    return first_batch
