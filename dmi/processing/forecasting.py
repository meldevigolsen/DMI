from sklearn.linear_model import LinearRegression
import pandas
import numpy


def linear_regression(series: pandas.Series, steps=0):
    linreg = LinearRegression()
    linreg.fit(series.index.values.reshape(-1, 1), series.values)
