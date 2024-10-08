from typing import List


def recall_at_k(labels: List[int], scores: List[float], k=5) -> float:
    """Return the recall"""
    sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    scores_k = sorted_indices[:k]
    relevant_elements = [i for i, label in enumerate(labels) if label == 1]
    relevant_at_k = set(scores_k) & set(relevant_elements)
    return len(relevant_at_k) / len(relevant_elements) if len(relevant_elements) > 0 else 0.0


def precision_at_k(labels: List[int], scores: List[float], k=5) -> float:
    """Return the precision"""
    sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    scores_k = sorted_indices[:k]
    relevant_elements = [i for i, label in enumerate(labels) if label == 1]
    relevant_at_k = set(scores_k) & set(relevant_elements)
    return len(relevant_at_k) / k if k > 0 else 0.0


def specificity_at_k(labels: List[int], scores: List[float], k=5) -> float:
    """ Specify at k"""
    sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    top_k_indices = sorted_indices[:k]

    # Определяем нерелевантные элементы (где label == 0)
    non_relevant_indices = [i for i, label in enumerate(labels) if label == 0]

    # Считаем True Negatives: нерелевантные элементы, которые не попали в топ-K
    true_negatives_at_k = len(set(non_relevant_indices) - set(top_k_indices))

    # Общее количество нерелевантных элементов
    total_non_relevant = len(non_relevant_indices)

    if total_non_relevant == 0:
        return 0.0  # Во избежание деления на ноль

    return true_negatives_at_k / total_non_relevant


def f1_at_k(labels: List[int], scores: List[float], k=5) -> float:
    """Returns the f1 at k"""
    p_k = precision_at_k(labels, scores, k)
    r_k = recall_at_k(labels, scores, k)
    return 2 * p_k * r_k / (p_k + r_k) if (p_k + r_k) != 0.0 else 0.0
