"""
Премиум-счет: овердрафт, дневной лимит снятия, фиксированная комиссия.

  * `DateTime.MinValue` -> date.min
  * `DateTime.Now.Date` -> date.today()
  * `Math.Abs(x)`       -> abs(x)
  * `private decimal _todayWithdrawn = 0;` -> self._today_withdrawn = Decimal("0") в __init__
    (в Python поля объекта создаются внутри __init__, а не в теле класса)
"""
from datetime import date
from decimal import Decimal

from banking_system.enums import Currency
from banking_system.exceptions import InsufficientFundsError, InvalidOperationError
from banking_system.models.bank_account import BankAccount
from banking_system.utils import to_decimal


class PremiumAccount(BankAccount):

    def __init__(self, owner_name: str, currency: Currency, overdraft_limit=10000,
                 withdrawal_limit=50000, fixed_commission=100, initial_balance=0,
                 account_id: str | None = None) -> None:
        super().__init__(owner_name, currency, initial_balance, account_id)
        self._overdraft_limit = to_decimal(overdraft_limit)
        self._withdrawal_limit = to_decimal(withdrawal_limit)
        self._fixed_commission = to_decimal(fixed_commission)
        self._today_withdrawn = Decimal("0")
        self._last_withdrawal_date = date.min

    @property
    def overdraft_limit(self):
        return self._overdraft_limit

    @property
    def withdrawal_limit(self):
        return self._withdrawal_limit

    @property
    def fixed_commission(self):
        return self._fixed_commission

    def _reset_daily_limit_if_needed(self) -> None:
        if self._last_withdrawal_date != date.today():
            self._today_withdrawn = Decimal("0")
            self._last_withdrawal_date = date.today()

    def withdraw(self, amount) -> None:
        amount = to_decimal(amount)
        self._validate_amount(amount)
        self._validate_account_status_for_operation()

        self._reset_daily_limit_if_needed()

        if self._today_withdrawn + amount > self._withdrawal_limit:
            raise InvalidOperationError(
                f"Превышен дневной лимит снятия: {self._withdrawal_limit} {self._currency}")

        total_amount = amount + self._fixed_commission
        available_funds = self.get_balance() + self._overdraft_limit

        if total_amount > available_funds:
            raise InsufficientFundsError()

        self._balance -= total_amount
        self._today_withdrawn += amount

        print(f"Счет {self._id}: успешно снято {amount} {self._currency} "
              f"(комиссия {self._fixed_commission} {self._currency}). "
              f"Новый баланс: {self._balance} {self._currency}")

        if self._balance < 0:
            print(f"Счет {self._id}: использован овердрафт. "
                  f"Доступно: {self.get_available_overdraft()} {self._currency}")

    def get_available_overdraft(self):
        balance = self.get_balance()
        if balance >= 0:
            return self._overdraft_limit
        return self._overdraft_limit - abs(balance)

    def get_account_info(self) -> str:
        return (f"Информация о премиум счете:\n"
                f"Тип счета: {type(self).__name__}\n"
                f"Владелец: {self._owner_name}\n"
                f"Номер счета: ****{self._last_four_digits()}\n"
                f"Полный номер: {self._id}\n"
                f"Статус: {self._status}\n"
                f"Баланс: {self.get_balance()} {self._currency}\n"
                f"Лимит овердрафта: {self._overdraft_limit} {self._currency}\n"
                f"Доступно овердрафта: {self.get_available_overdraft()} {self._currency}\n"
                f"Дневной лимит снятия: {self._withdrawal_limit} {self._currency}\n"
                f"Снято сегодня: {self._today_withdrawn} {self._currency}\n"
                f"Фиксированная комиссия: {self._fixed_commission} {self._currency}\n"
                f"Валюта: {self._currency}")

    def __str__(self) -> str:
        balance = self.get_balance()
        # Тернарный оператор: C# `cond ? a : b`  ->  Python `a if cond else b`
        overdraft_info = f" (ОВЕРДРАФТ: {abs(balance)})" if balance < 0 else ""
        return (f"{type(self).__name__} - {self._owner_name} (****{self._last_four_digits()}) | "
                f"Статус: {self._status} | Баланс: {balance} {self._currency}{overdraft_info} | "
                f"Лимит: {self._withdrawal_limit} | Комиссия: {self._fixed_commission}")
