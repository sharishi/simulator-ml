from __future__ import annotations
from typing import List
import numpy as np


class BankMetrics:
    """
    A class to represent bank metrics.

    Attributes
    ----------
    global_bank_rate : float
        The global bank rate applicable to all accounts.
    accounts : List[BankMetrics]
        A list of BankMetrics instances representing bank accounts.

    Methods
    -------
    __init__(name: str, balance: float):
        Initializes a new BankMetrics instance with a name and balance.
    adjust_global_bank_rate(new_rate: float):
        Method to adjust the global bank rate.
    calculate_avg_balance() -> float:
        Method to calculate the average balance across all accounts.
    calculate_interest(account: BankMetrics) -> float:
        Method to calculate interest for a given account.
    """

    global_bank_rate: float = 15.0
    accounts: List[BankMetrics] = []

    def __init__(self, name: str, balance: float):
        self.name = name
        self.balance = balance
        BankMetrics.accounts.append(self)

    @staticmethod
    def adjust_global_bank_rate(new_rate: float):
        """Adjust global bank rate"""
        BankMetrics.global_bank_rate = new_rate

    @classmethod
    def calculate_avg_balance(cls) -> float:
        """Calculate average balance"""
        balances = [account.balance for account in cls.accounts]
        return np.mean(balances)

    @classmethod
    def calculate_interest(cls, account: BankMetrics) -> float:
        """Calculate interests"""
        return round(account.balance * (cls.global_bank_rate / 100), 2)
