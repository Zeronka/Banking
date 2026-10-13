"""
Статусы счета.

C#:
    public enum AccountStatus { Active, Frozen, Closed }

В Python перечисления делаются через класс, наследующий Enum.
"""
from enum import Enum


class AccountStatus(Enum):
    ACTIVE = "Active"
    FROZEN = "Frozen"
    CLOSED = "Closed"

    # В C# enum при выводе в строку печатает своё имя ("Active").
    # В Python по умолчанию печаталось бы "AccountStatus.ACTIVE",
    # поэтому переопределяем __str__ (аналог ToString() в C#).
    def __str__(self) -> str:
        return self.value
