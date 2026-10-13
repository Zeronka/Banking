"""
Пакет enums (аналог пространства имён BankingSystem.Enums в C#).

Файл __init__.py превращает папку в пакет и позволяет писать короткий импорт:
    from banking_system.enums import Currency
вместо
    from banking_system.enums.currency import Currency
"""
from .account_status import AccountStatus
from .currency import Currency

__all__ = ["AccountStatus", "Currency"]
