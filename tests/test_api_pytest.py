import api
from dmi.fetching import objects
from dmi.processing import data_instantiator
import datetime


def test_get_data_batch():
    country = objects.Countries.DENMARK.value
    area = country.areas[1]
    datatype = objects.DataType.TEMPERATURE

    date = datetime.datetime.strptime('1/1-2019', '%d/%m-%Y')
    data_batch = api.get_data_batch(
        area, datatype, objects.Interval.HOURLY, date)
    assert isinstance(data_batch, data_instantiator.DataBatch)


def test_get_yearly_data_batch():
    country = objects.Countries.DENMARK.value
    area = country.areas[1]
    datatype = objects.DataType.TEMPERATURE

    data_batch = api.get_yearly_data_batch(area, datatype, 2011, 2019)
    assert isinstance(data_batch, data_instantiator.DataBatch)


def test_get_data_timespan():
    country = objects.Countries.DENMARK.value
    area = country.areas[1]
    datatype = objects.DataType.TEMPERATURE

    start_date = datetime.datetime.strptime('1/1-2019', '%d/%m-%Y')
    end_date = datetime.datetime.strptime('1/2-2019', '%d/%m-%Y')

    data_batch = api.get_data_timespan(
        area, datatype, objects.Interval.HOURLY, start_date, end_date)
    assert isinstance(data_batch, data_instantiator.DataBatch)
