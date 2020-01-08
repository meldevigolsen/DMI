from matplotlib import pyplot
from pandas.plotting import register_matplotlib_converters

from dmi.processing import data_instantiator

register_matplotlib_converters()


def __plot_dmi_series(dmi_series: data_instantiator.DMISeries, ax: pyplot.Axes):
    line_style = ''
    if isinstance(dmi_series, data_instantiator.PredictedSeries):
        line_style = '--'
    ax.plot(dmi_series.series, line_style, label=f'{dmi_series.description}')


def __plot_batch(batch: data_instantiator.Batch, ax: pyplot.Axes):
    for dmi_series in batch.dmi_series_list:
        __plot_dmi_series(dmi_series, ax)


def __setup_ax(ax: pyplot.Axes, batch: data_instantiator.Batch):
    ax.set_title(f'{batch.datatype.danish_name} ({batch.interval.danish_name})')
    ax.set_ylabel(batch.dmi_series_list[0].unit)
    for tick in ax.get_xticklabels():
        tick: pyplot.Text
        tick.set_horizontalalignment('right')
        tick.set_rotation('45')
        tick.set_rotation_mode('anchor')
    ax.grid()
    ax.legend()


def __setup_fig(fig: pyplot.Figure, batch: data_instantiator.Batch):
    fig.suptitle(batch.area.name, y=1)
    fig.set_size_inches(10, 5)


def plot_batch(batch: data_instantiator.Batch):
    fig: pyplot.Figure
    ax: pyplot.Axes
    fig, ax = pyplot.subplots()
    __plot_batch(batch, ax)
    __setup_ax(ax, batch)
    __setup_fig(fig, batch)
    pyplot.show()


def plot_double(first_batch: data_instantiator.Batch, second_batch: data_instantiator.Batch):
    fig: pyplot.Figure
    ax: pyplot.Axes
    fig, ax = pyplot.subplots()
    __plot_batch(first_batch, ax)
    __plot_batch(second_batch, ax)
    __setup_ax(ax, first_batch)
    __setup_fig(fig, first_batch)
    pyplot.show()
