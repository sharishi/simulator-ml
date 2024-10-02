from typing import List

import numpy as np

from typing import List
import numpy as np


def compute_dcg(relevance: List[float], k: int, method: str) -> float:
    """Compute Discounted Cumulative Gain (DCG)

    Parameters
    ----------
    relevance : List[float]
        Relevance scores
    method : str
        Metric implementation method

    Returns
    -------
    float
        DCG score
    """
    relevance = np.array(relevance[:min(k, len(relevance))])

    if method == "standard":
        return np.sum(relevance / np.log2(np.arange(2, k + 2)))
    elif method == "industry":
        return np.sum((np.power(2, relevance) - 1) / np.log2(np.arange(2, k + 2)))
    else:
        raise ValueError


def compute_idcg(relevance: List[float], k: int, method: str) -> float:
    """Compute Ideal Discounted Cumulative Gain (iDCG)

    Parameters
    ----------
    relevance : List[float]
        Relevance scores
    method : str
        Metric implementation method

    Returns
    -------
    float
        iDCG score
    """
    sorted_relevance = sorted(relevance, reverse=True)
    return compute_dcg(sorted_relevance, k, method)


def normalized_dcg(relevance: List[float], k: int, method: str = "standard") -> float:
    """Normalized Discounted Cumulative Gain

    Parameters
    ----------
    relevance : List[float]
        Video relevance list
    k : int
        Count relevance to compute
    method : str, optional
        Metric implementation method

    Returns
    -------
    float
        Metric score
    """
    if k <= 0:
        return 0.0

    if len(relevance) == 0:
        return 0.0

    dcg = compute_dcg(relevance,k, method)
    idcg = compute_idcg(relevance,k, method)

    return dcg / idcg if idcg > 0 else 0.0


def avg_ndcg(list_relevances: List[List[float]], k: int, method: str = 'standard') -> float:
    """average nDCG

    Parameters
    ----------
    list_relevances : List[List[float]]
        Video relevance matrix for various queries
    k : int
        Count relevance to compute
    method : str, optional
        Metric implementation method, takes the values\
        standard - adds weight to the denominator\
        industry - adds weights to the numerator and denominator\
        raise ValueError - for any value

    Returns
    -------
    score : float
        Metric score
    """
    sum = 0
    if len(list_relevances) == 0:
        return 0.0
    for one_list in list_relevances:
        sum += normalized_dcg(one_list, k, method)

    return sum/len(list_relevances)