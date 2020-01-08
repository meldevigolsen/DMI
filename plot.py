import pandas
from matplotlib import pyplot
from dmi.fetching import objects
from dmi.processing import data_instantiator
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def __plot_dmi_series(dmi_series: data_instantiator.DMISeries, ax: pyplot.Axes):
    line_style = ''
    if isinstance(dmi_series, data_instantiator.PredictedSeries):
        line_style = '--'
    ax.plot(dmi_series.series, line_style, label=f'{dmi_series.description}')


def __plot_batch(batch: data_instantiator.Batch, ax: pyplot.Axes):
    for dmi_series in batch.dmi_series_list:
        __plot_dmi_series(dmi_series, ax)
    ax.grid()
    ax.legend()


def plot_batch(batch: data_instantiator.Batch):
    fig: pyplot.Figure
    ax: pyplot.Axes
    fig, ax = pyplot.subplots()
    __plot_batch(batch, ax)
    pyplot.show()


def plot_double(first_batch: data_instantiator.Batch, second_batch: data_instantiator.Batch):
    fig: pyplot.Figure
    ax: pyplot.Axes
    fig, ax = pyplot.subplots()
    __plot_batch(first_batch, ax)
    __plot_batch(second_batch, ax)
    pyplot.show()
