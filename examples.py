import datetime

import api
import plot
from dmi.fetching import objects
from dmi.processing import forecasting

country = objects.Countries.DENMARK.value
area = country.areas[1]

start_date = datetime.datetime.strptime('1/1-2019', '%d/%m-%Y')
end_date = datetime.datetime.strptime('5/1-2019', '%d/%m-%Y')


def plot_batch():
    data_batch = api.get_data_batch(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date)
    plot.plot_batch(data_batch)


def plot_batch_linreg():
    data_batch = api.get_data_batch(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date)
    prediction = forecasting.linear_regression(data_batch)
    plot.plot_batch_with_prediction(data_batch, prediction)


def plot_batch_linreg_steps():
    data_batch = api.get_data_batch(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date)
    prediction = forecasting.linear_regression(data_batch, 10)
    plot.plot_batch_with_prediction(data_batch, prediction)


def plot_batch_poly_linreg():
    data_batch = api.get_data_batch(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date)
    prediction = forecasting.polynomial_linear_regression(data_batch, 2)
    plot.plot_batch_with_prediction(data_batch, prediction)


def plot_timespan_batch():
    data_batch = api.get_data_timespan(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date,
                                       end_date)
    plot.plot_batch(data_batch)


def plot_yearly_batch():
    data_batch = api.get_yearly_data_batch(area, objects.DataTypes.TEMPERATURE, 2011, 2019)
    plot.plot_batch(data_batch)


def plot_timespan_batch_arima():
    data_batch = api.get_data_timespan(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date,
                                       end_date)
    prediction = forecasting.arima_prediction(data_batch, 24)
    plot.plot_batch_with_prediction(data_batch, prediction)


def plot_timespan_batch_linreg():
    data_batch = api.get_data_timespan(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date,
                                       end_date)
    prediction = forecasting.linear_regression(data_batch)
    plot.plot_batch_with_prediction(data_batch, prediction)


def plot_timespan_batch_poly_linreg():
    data_batch = api.get_data_timespan(area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date,
                                       end_date)
    prediction = forecasting.polynomial_linear_regression(data_batch, 2)
    plot.plot_batch_with_prediction(data_batch, prediction)


# plot_timespan_batch_linreg()
# plot_timespan_batch_poly_linreg()
plot_timespan_batch_arima()
