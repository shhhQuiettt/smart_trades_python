from math import floor


def floor_decimal(n, decimal=0):
    return floor(n * 10 ** decimal) / 10 ** decimal


def absolute_error(given, expected):
    "Returns absolute error rounded to 10 digits"
    return round(abs(given - expected), 10)
