from dmi.fetching import objects
import api
import datetime
import plot
from dmi.processing import forecasting

country = objects.Countries.DENMARK.value
area = country.areas[1]
datatype = objects.DataType.TEMPERATURE

start_date = datetime.datetime.strptime('1/1-2019', '%d/%m-%Y')
#end_date = datetime.datetime.strptime('1/2-2019', '%d/%m-%Y')

data_batch = api.get_data_batch(
    area, datatype, objects.Interval.HOURLY, start_date)
prediction = forecasting.linear_regression(data_batch)
plot.plot_double(data_batch, prediction)