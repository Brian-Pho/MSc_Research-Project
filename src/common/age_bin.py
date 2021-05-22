from collections import namedtuple

import numpy as np

Bin = namedtuple("Bin", "X y")


def bin_by_age(X, y, ages):
    X_bin_1, y_bin_1 = _select_data(X, y, np.where(ages <= 9))
    X_bin_2, y_bin_2 = _select_data(X, y, np.where(
        np.logical_and(ages <= 12, ages > 9)))
    X_bin_3, y_bin_3 = _select_data(X, y, np.where(ages > 12))

    return Bin(X_bin_1, y_bin_1), Bin(X_bin_2, y_bin_2), Bin(X_bin_3, y_bin_3)


def _select_data(X, y, indices):
    return X[indices], y[indices]
