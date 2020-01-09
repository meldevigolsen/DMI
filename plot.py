from matplotlib import pyplot
from pandas.plotting import register_matplotlib_converters

from dmi.processing import data_instantiator

register_matplotlib_converters()
__color_order = {0: 'g', 1: 'r', 2: 'b'}


def __plot_forecast(ax, forecast, color, description):
    ax.plot(forecast, linestyle='dashed', color=color, label=f'{description} forecast')


def __plot_dmi_series(dmi_series: data_instantiator.DMISeries, ax: pyplot.Axes, color: str):
    if isinstance(dmi_series, data_instantiator.DataSeries):
        dmi_series: data_instantiator.DataSeries
        ax.plot(dmi_series.series, linestyle='solid', color=color, label=f'{dmi_series.description}')
    elif isinstance(dmi_series, data_instantiator.LinearRegressionSeries):
        dmi_series: data_instantiator.LinearRegressionSeries
        ax.plot(dmi_series.series, linestyle='dotted', color=color,
                label=f'{dmi_series.description}\n{dmi_series.linear_regression_description}')
        ax.plot(dmi_series.forecast, linestyle='dashed', color=color, label=f'{dmi_series.description} forecast')
    elif isinstance(dmi_series, data_instantiator.ARIMASeries):
        dmi_series: data_instantiator.ARIMASeries
        ax.plot(dmi_series.series, linestyle='dotted', color=color,
                label=f'{dmi_series.description}\n{dmi_series.arima_description}')
        ax.plot(dmi_series.forecast, linestyle='dashed', color=color, label=f'{dmi_series.description} forecast')
        intervals = dmi_series.confidence_intervals
        ax.fill_between()


def __plot_batch(batch: data_instantiator.Batch, ax: pyplot.Axes):
    color_code = 0
    for dmi_series in batch.dmi_series_list:
        __plot_dmi_series(dmi_series, ax, __color_order[color_code])
        color_code += 1


def __setup_ax(ax: pyplot.Axes, batch: data_instantiator.Batch):
    ax.set_title(f'{batch.datatype.danish_name} ({batch.interval.danish_name})', loc='left')
    ax.set_ylabel(batch.dmi_series_list[0].unit)
    for tick in ax.get_xticklabels():
        tick: pyplot.Text
        tick.set_horizontalalignment('right')
        tick.set_rotation('45')
        tick.set_rotation_mode('anchor')
    ax.grid()
    ax.legend(bbox_to_anchor=(1, 1))


def __setup_fig(fig: pyplot.Figure, batch: data_instantiator.Batch):
    fig.suptitle(batch.area.name)
    fig.set_size_inches(10, 5)


def plot_batch(batch: data_instantiator.Batch):
    fig: pyplot.Figure
    ax: pyplot.Axes
    fig, ax = pyplot.subplots()
    __plot_batch(batch, ax)
    __setup_ax(ax, batch)
    __setup_fig(fig, batch)
    pyplot.show()


def plot_batch_with_prediction(first_batch: data_instantiator.DataBatch,
                               second_batch: data_instantiator.PredictedBatch):
    fig: pyplot.Figure
    ax: pyplot.Axes
    fig, ax = pyplot.subplots()
    __plot_batch(first_batch, ax)
    __plot_batch(second_batch, ax)
    __setup_ax(ax, first_batch)
    __setup_fig(fig, first_batch)
    pyplot.show()
