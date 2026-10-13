"""
Валюты.

C#:
    public enum Currency { RUB, USD, EUR, KZT, CNY }
"""
from enum import Enum


class Currency(Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    KZT = "KZT"
    CNY = "CNY"

    def __str__(self) -> str:
        return self.value
