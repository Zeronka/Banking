"""
Вспомогательная функция для денег.

В C# для денег используется тип decimal (литерал 5.5m).
В Python его аналог — decimal.Decimal. Обычный float для денег
не подходит: 0.1 + 0.2 == 0.30000000000000004.

Чтобы можно было передавать в методы и int (1000), и Decimal("5.5"),
приводим любое число к Decimal через строку: Decimal(str(5.5)) == Decimal("5.5").
"""
from decimal import Decimal


def to_decimal(value) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))
