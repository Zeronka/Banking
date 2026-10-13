"""
Обычный банковский счет.

Важное отличие: в C# у класса ДВА конструктора (перегрузка):
    BankAccount(string ownerName, Currency currency, decimal initialBalance = 0)
    BankAccount(string id, string ownerName, Currency currency, decimal initialBalance = 0)
В Python перегрузки нет: у класса один __init__. Поэтому id сделан
необязательным именованным параметром account_id=None. Если его не передали,
ID генерируется автоматически, как в первом конструкторе C#.

Другие соответствия:
  * `private static readonly Random _random` -> модуль random
  * `private static string ValidateId(...)`  -> @staticmethod _validate_id(...)
  * `Console.WriteLine(...)`                 -> print(...)
  * `string.IsNullOrWhiteSpace(s)`           -> not s or not s.strip()
  * `switch (Status) { case ...: }`          -> if / elif (или match в Python 3.10+)
  * `public decimal GetBalance() => Balance;` -> def get_balance(self): return self._balance
"""
import random

from banking_system.enums import AccountStatus, Currency
from banking_system.exceptions import (
    AccountClosedError,
    AccountFrozenError,
    InsufficientFundsError,
    InvalidOperationError,
)
from banking_system.models.abstract_account import AbstractAccount
from banking_system.utils import to_decimal


class BankAccount(AbstractAccount):
    _SHORT_ID_LENGTH = 8      # private const int SHORT_ID_LENGTH = 8

    def __init__(self, owner_name: str, currency: Currency, initial_balance=0, account_id: str | None = None) -> None:
        if account_id is None:
            account_id = BankAccount._generate_short_id()

        # C#: : base(ValidateId(id), ValidateOwnerName(ownerName), ...)
        super().__init__(
            BankAccount._validate_id(account_id),
            BankAccount._validate_owner_name(owner_name),
            BankAccount._validate_initial_balance(to_decimal(initial_balance)),
        )
        self._currency = currency

    @property
    def currency(self) -> Currency:
        return self._currency

    # ---------- статические вспомогательные методы ----------
    @staticmethod
    def _generate_short_id() -> str:
        chars = "0123456789"
        # Генератор списка вместо цикла for + StringBuilder
        return "".join(random.choice(chars) for _ in range(BankAccount._SHORT_ID_LENGTH))

    @staticmethod
    def _validate_id(account_id: str) -> str:
        if not account_id or not account_id.strip():
            raise InvalidOperationError("ID счета не может быть пустым")   # throw -> raise
        return account_id

    @staticmethod
    def _validate_owner_name(owner_name: str) -> str:
        if not owner_name or not owner_name.strip():
            raise InvalidOperationError("Имя владельца не может быть пустым")
        if len(owner_name) < 2:                                            # .Length -> len()
            raise InvalidOperationError("Имя владельца слишком короткое")
        return owner_name.strip()                                          # .Trim() -> .strip()

    @staticmethod
    def _validate_initial_balance(balance):
        if balance < 0:
            raise InvalidOperationError("Начальный баланс не может быть отрицательным")
        return balance

    # ---------- protected-проверки (доступны наследникам) ----------
    def _validate_amount(self, amount) -> None:
        if amount <= 0:
            raise InvalidOperationError("Сумма должна быть положительной")

    def _validate_account_status_for_operation(self) -> None:
        if self._status == AccountStatus.FROZEN:
            raise AccountFrozenError()
        if self._status == AccountStatus.CLOSED:
            raise AccountClosedError()

    # ---------- операции ----------
    def deposit(self, amount) -> None:
        amount = to_decimal(amount)
        self._validate_amount(amount)
        self._validate_account_status_for_operation()

        self._balance += amount
        print(f"Счет {self._id}: успешно пополнен на {amount} {self._currency}. "
              f"Новый баланс: {self._balance} {self._currency}")

    def withdraw(self, amount) -> None:
        amount = to_decimal(amount)
        self._validate_amount(amount)
        self._validate_account_status_for_operation()

        if self._balance < amount:
            raise InsufficientFundsError()

        self._balance -= amount
        print(f"Счет {self._id}: успешно снято {amount} {self._currency}. "
              f"Новый баланс: {self._balance} {self._currency}")

    def freeze_account(self) -> None:
        if self._status == AccountStatus.CLOSED:
            raise InvalidOperationError("Нельзя заморозить закрытый счет")
        self._status = AccountStatus.FROZEN
        print(f"Счет {self._id} заморожен")

    def unfreeze_account(self) -> None:
        if self._status == AccountStatus.FROZEN:
            self._status = AccountStatus.ACTIVE
            print(f"Счет {self._id} разморожен")

    def close_account(self) -> None:
        if self._balance != 0:
            raise InvalidOperationError("Нельзя закрыть счет с ненулевым балансом")
        self._status = AccountStatus.CLOSED
        print(f"Счет {self._id} закрыт")

    def get_account_info(self) -> str:
        return (f"Информация о счете:\n"
                f"Тип счета: {type(self).__name__}\n"
                f"Владелец: {self._owner_name}\n"
                f"Номер счета: ****{self._last_four_digits()}\n"
                f"Полный номер: {self._id}\n"
                f"Статус: {self._status}\n"
                f"Баланс: {self._balance} {self._currency}\n"
                f"Валюта: {self._currency}")

    def __str__(self) -> str:
        return (f"{type(self).__name__} - {self._owner_name} (****{self._last_four_digits()}) | "
                f"Статус: {self._status} | Баланс: {self._balance} {self._currency}")

    def get_balance(self):
        return self._balance
