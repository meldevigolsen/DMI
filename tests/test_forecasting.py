import datetime
from unittest import TestCase

import api
from dmi.fetching import objects
from dmi.processing import forecasting, data_instantiator


class TestForecasting(TestCase):
    def setUp(self) -> None:
        country = objects.Countries.DENMARK.value
        area = country.areas[1]
        start_date = datetime.datetime.strptime('1/1-2019', '%d/%m-%Y')
        data_batch = api.get_data_batch(
            area, objects.DataTypes.TEMPERATURE, objects.Intervals.HOURLY, start_date)
        self.data_batch = data_batch

    def test_polynomial_linear_regression(self):
        prediction_2 = forecasting.polynomial_linear_regression(self.data_batch, 2)
        self.assertIsInstance(prediction_2, data_instantiator.PredictedBatch)
        prediction_3 = forecasting.polynomial_linear_regression(self.data_batch, 3)
        self.assertIsInstance(prediction_3, data_instantiator.PredictedBatch)
        prediction_10 = forecasting.polynomial_linear_regression(self.data_batch, 10)
        self.assertIsInstance(prediction_10, data_instantiator.PredictedBatch)
        step_prediction_2 = forecasting.polynomial_linear_regression(self.data_batch, 2, 10)
        self.assertIsInstance(step_prediction_2, data_instantiator.PredictedBatch)
        step_prediction_3 = forecasting.polynomial_linear_regression(self.data_batch, 3, 20)
        self.assertIsInstance(step_prediction_3, data_instantiator.PredictedBatch)
        step_prediction_10 = forecasting.polynomial_linear_regression(self.data_batch, 10, 30)
        self.assertIsInstance(step_prediction_10, data_instantiator.PredictedBatch)

    def test_linear_regression(self):
        prediction = forecasting.linear_regression(self.data_batch)
        self.assertIsInstance(prediction, data_instantiator.PredictedBatch)
        prediction_2 = forecasting.linear_regression(self.data_batch, 2)
        self.assertIsInstance(prediction_2, data_instantiator.PredictedBatch)
        prediction_10 = forecasting.linear_regression(self.data_batch, 10)
        self.assertIsInstance(prediction_10, data_instantiator.PredictedBatch)
