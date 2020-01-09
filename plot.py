from typing import List, Optional

from matplotlib import pyplot
from pandas.plotting import register_matplotlib_converters

from dmi.processing import data_instantiator

register_matplotlib_converters()
__color_order = {0: 'g', 1: 'r', 2: 'b'}


def __plot_dmi_series(dmi_series: data_instantiator.DMISeries, ax: pyplot.Axes, is_test_data=False,
                      exclude_training=False):
    if isinstance(dmi_series, data_instantiator.DataSeries):
        dmi_series: data_instantiator.DataSeries
        ax.plot(dmi_series.series, linestyle='solid', label=f'{"Test data" if is_test_data else "Virkelig data"}')
    elif isinstance(dmi_series, data_instantiator.PredictedSeries):
        dmi_series: data_instantiator.PredictedSeries
        if not exclude_training:
            ax.plot(dmi_series.series, linestyle='dotted', label=f'In-sample prognose')
        ax.plot(dmi_series.forecast, linestyle='dashed', label=f'Prognose frem i tid')
        if isinstance(dmi_series, data_instantiator.ARIMASeries):
            dmi_series: data_instantiator.ARIMASeries
            intervals = dmi_series.confidence_intervals
            ax.fill_between(intervals.index, intervals['upper_limit'], intervals['lower_limit'], alpha=.5,
                            label=f'95% sikkerhed')


def __plot_batch(batch: data_instantiator.Batch, ax: pyplot.Axes):
    color_code = 0
    for dmi_series in batch.dmi_series_list:
        __plot_dmi_series(dmi_series, ax)
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


def __setup_multi_ax(ax: pyplot.Axes, dmi_series: data_instantiator.DMISeries):
    ax.set_title(f'{dmi_series.description}', loc='left')
    ax.set_ylabel(dmi_series.unit)
    for tick in ax.get_xticklabels():
        tick: pyplot.Text
        tick.set_horizontalalignment('right')
        tick.set_rotation('45')
        tick.set_rotation_mode('anchor')
    ax.grid()
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))


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


def plot_prediction(data_batch: data_instantiator.DataBatch,
                    predicted_batch: data_instantiator.PredictedBatch,
                    test_data_batch: Optional[data_instantiator.DataBatch] = None, exclude_training=False):
    number_of_series = len(data_batch.data_series_list)
    fig: pyplot.Figure
    axes: List[pyplot.Axes]
    fig, axes = pyplot.subplots(number_of_series, sharex='all')
    if number_of_series == 1:
        # noinspection PyTypeChecker
        axes = [axes]
    for i in range(number_of_series):
        ax = axes[i]
        predicted_series = predicted_batch.predicted_series_list[i]
        __plot_dmi_series(predicted_series, ax, exclude_training=exclude_training)
        if not exclude_training:
            data_series = data_batch.data_series_list[i]
            __plot_dmi_series(data_series, ax)
        if test_data_batch is not None:
            __plot_dmi_series(test_data_batch.data_series_list[i], ax, is_test_data=True)
        __setup_multi_ax(ax, predicted_series)
    fig.suptitle(data_batch.area.name)
    fig.set_size_inches(10, (3 * number_of_series) if number_of_series > 1 else 5)
    pyplot.show()
