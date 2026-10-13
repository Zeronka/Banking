from abc import ABC, abstractmethod
from decimal import Decimal

from banking_system.enums import AccountStatus


class AbstractAccount(ABC):

    def __init__(self, account_id: str, owner_name: str, initial_balance: Decimal = Decimal("0")) -> None:
        self._id = account_id
        self._owner_name = owner_name
        self._balance = initial_balance
        self._status = AccountStatus.ACTIVE

    @property
    def id(self) -> str:
        return self._id

    @property
    def owner_name(self) -> str:
        return self._owner_name

    @property
    def status(self) -> AccountStatus:
        return self._status

    @abstractmethod
    def deposit(self, amount) -> None: ...

    @abstractmethod
    def withdraw(self, amount) -> None: ...

    @abstractmethod
    def get_account_info(self) -> str: ...

    def _last_four_digits(self) -> str:
        return self._id[-4:]

    def __str__(self) -> str:
        return (f"Тип: {type(self).__name__}, Клиент: {self._owner_name}, "
                f"Номер: ****{self._last_four_digits()}, "
                f"Статус: {self._status}, Баланс: {self._balance}")
