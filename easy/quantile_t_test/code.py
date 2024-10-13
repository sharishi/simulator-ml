from typing import List
from typing import Tuple

import numpy as np
from scipy.stats import ttest_ind


def bootstrapped_mean(x: List[float], n_bootstraps: int = 1000) -> List[float]:
    """Bootstrapped median distribution"""
    bootstrapped_means = []

    for _ in range(n_bootstraps):
        bootstrapped_sample = np.random.choice(x, size=len(x), replace=True)
        bootstrapped_means.append(np.mean(bootstrapped_sample))

    return bootstrapped_means


def quantile_ttest(
    control: List[float],
    experiment: List[float],
    alpha: float = 0.05,
    quantile: float = 0.95,
    n_bootstraps: int = 1000,
) -> Tuple[float, bool]:
    """
    Bootstrapped t-test for quantiles of two samples.
    """
    control_bootstraps = bootstrapped_mean(control, n_bootstraps)
    experiment_bootstraps = bootstrapped_mean(experiment, n_bootstraps)

    # Вычисляем квантиль для каждого бутстрепа
    control_q = np.quantile(control_bootstraps, quantile)
    experiment_q = np.quantile(experiment_bootstraps, quantile)

    # t-test для массивов бутстрепированных выборок
    _, p_value = ttest_ind(control_bootstraps, experiment_bootstraps)

    # Сравниваем p_value с уровнем значимости alpha
    result = bool(p_value <= alpha)
    return p_value, result
