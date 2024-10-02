import numpy as np


def smape(y_true: np.array, y_pred: np.array) -> float:

    """Fix bugs"""
    den = np.abs(y_true) + np.abs(y_pred)
    den = np.where(den == 0, 1, den)

    return np.mean(2 * np.abs(y_true - y_pred) / den)


