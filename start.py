from dmi.fetching import objects
import api
import datetime
import plot
country = objects.Countries.DENMARK.value
area = country.areas[1]
datatype = objects.DataType.TEMPERATURE

date = datetime.datetime.strptime('1/1-2019','%d/%m-%Y')
data_batch = api.get_data_batch(area, datatype, objects.Interval.HOURLY, date)
plot.plot_data_batch(data_batch)