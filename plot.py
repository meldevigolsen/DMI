from matplotlib import pyplot
from dmi.fetching import objects
from dmi.processing import data_instantiator
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def __plot_data_series(data_series: data_instantiator.DataSeries, ax: pyplot.Axes):
    ax.plot(data_series.to_pandas_series())


def __plot_data_batch(data_batch: data_instantiator.DataBatch, ax: pyplot.Axes):
    for data_series in data_batch.data_series:
        __plot_data_series(data_series, ax)
    ax.grid()
    ax.legend()


def plot_data_batch(data_batch: data_instantiator.DataBatch):
    fig: pyplot.Figure
    ax: pyplot.Axes
    fig, ax = pyplot.subplots()
    __plot_data_batch(data_batch, ax)
    pyplot.show()

