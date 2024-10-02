import numpy as np


def ltv_error(y_true: np.array, y_pred: np.array) -> float:
    """LTVTurnover error function

    Args:
        y_true (np.ndarray): True values
        y_pred (np.ndarray): Pred values

    Returns:
        float: Turnover error
    """

    squared_true = y_true ** 2
    squared_pred = y_pred ** 2
    error = np.sqrt(np.sum(np.abs(squared_true - squared_pred)))
    return error


