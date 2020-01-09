import datetime

import api
import plot
from dmi.fetching import objects
from dmi.processing import forecasting

country = objects.Countries.DENMARK.value
area = country.areas[1]

start_date = datetime.datetime.strptime('1/1-2019', '%d/%m-%Y')
end_date = datetime.datetime.strptime('1/2-2019', '%d/%m-%Y')

data_batch = api.get_data_batch(
    area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date)
prediction = forecasting.linear_regression(data_batch, 10)
plot.plot_prediction(data_batch, prediction)
