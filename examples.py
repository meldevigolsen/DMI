import datetime

import api
import plot
from dmi.fetching import objects
from dmi.processing import forecasting

country = objects.Countries.DENMARK.value
area = country.areas[1]

start_date = datetime.datetime(2019, 1, 1)
end_date = datetime.datetime(2019, 1, 10)


def plot_batch():
    data_batch = api.get_data_batch(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date)
    plot.plot_batch(data_batch)


def plot_batch_linreg():
    data_batch = api.get_data_batch(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date)
    prediction = forecasting.linear_regression(data_batch)
    plot.plot_prediction(data_batch, prediction)


def plot_batch_linreg_steps():
    data_batch = api.get_data_batch(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date)
    prediction = forecasting.linear_regression(data_batch, 10)
    plot.plot_prediction(data_batch, prediction)


def plot_batch_poly_linreg():
    data_batch = api.get_data_batch(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date)
    prediction = forecasting.polynomial_linear_regression(data_batch, 2)
    plot.plot_prediction(data_batch, prediction)


def plot_timespan_batch():
    data_batch = api.get_data_timespan(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date,
                                       end_date)
    plot.plot_batch(data_batch)


def plot_yearly_batch():
    data_batch = api.get_yearly_data_batch(area, objects.DataTypes.TEMPERATURE, 2011, 2019)
    plot.plot_batch(data_batch)


def plot_timespan_batch_arima():
    data_batch = api.get_data_timespan(area, objects.DataTypes.HUMIDITY, objects.Intervals.HOURLY, start_date,
                                       end_date)
    prediction = forecasting.arima_prediction(data_batch, 24)
    plot.plot_prediction(data_batch, prediction)


def plot_timespan_batch_linreg():
    data_batch = api.get_data_timespan(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date,
                                       end_date)
    prediction = forecasting.linear_regression(data_batch)
    plot.plot_prediction(data_batch, prediction)


def plot_timespan_batch_poly_linreg():
    data_batch = api.get_data_timespan(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date,
                                       end_date)
    prediction = forecasting.polynomial_linear_regression(data_batch, 2)
    plot.plot_prediction(data_batch, prediction)


def plot_timespan_batch_sarimax():
    data_batch = api.get_data_timespan(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date,
                                       end_date)
    prediction = forecasting.sarimax_prediction(data_batch, 24, 24)
    plot.plot_prediction(data_batch, prediction)


def plot_timespan_batch_sarimax_with_test():
    predict_length = 24
    test_start_date = end_date + datetime.timedelta(days=1)
    test_end_date = end_date + datetime.timedelta(hours=predict_length)
    datatype = objects.DataTypes.PRECIPITATION
    data_batch = api.get_data_timespan(area, datatype, objects.Intervals.HOURLY, start_date, end_date)
    test_data_batch = api.get_data_timespan(area, datatype, objects.Intervals.HOURLY, test_start_date, test_end_date)
    prediction = forecasting.sarimax_prediction(data_batch, 24, predict_length)
    plot.plot_prediction(data_batch, prediction, test_data_batch=test_data_batch)


# plot_timespan_batch_linreg()
# plot_timespan_batch_poly_linreg()
plot_timespan_batch_sarimax_with_test()
