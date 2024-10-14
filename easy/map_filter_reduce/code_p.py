from typing import List
from functools import reduce


def sales_with_tax(sales: List[float], tax_rate: float, threshold: float = 300) -> List[float]:
    """Filter sales by tax rate"""
    return list(map(lambda x: x * (1 + tax_rate), filter(lambda x: x > threshold, sales)))


def sum_sales(sales: List[float], threshold: float = 300) -> float:
    """Sum sales filtered by tax rate"""
    return float(reduce(lambda x, y: x + y, filter(lambda x: x > threshold, sales)))


def average_age(ages: List[int], threshold: int = 30) -> float:
    """Average age calculate"""
    filtered_ages = list(filter(lambda x: x > threshold, ages))
    sum_of_ages = reduce(lambda x, y: x + y, filtered_ages)
    return sum_of_ages / len(filtered_ages)


def increased_prices(prices: List[float], increase_rate: float = 0.2, threshold: float = 300) -> List[float]:
    """Show filtered increase prices"""
    new_prices = map(lambda x: x + x*increase_rate, prices)
    return list(filter(lambda x: x > threshold,  new_prices))


def weighted_sale_price(sales: List[float]) -> float:
    """Returns the weighted sale price"""
    nom = reduce(lambda x, y: x + y, list(map(lambda x: x[0]*x[1], sales)))
    den = reduce(lambda x, y: x + y, list(map(lambda sale: sale[1], sales)))
    return nom / den if den > 0 else 0
