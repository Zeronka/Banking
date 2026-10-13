"""
Сберегательный счет: неснижаемый остаток + ежемесячные проценты.

C#: public class SavingAccount : BankAccount
Python: class SavingAccount(BankAccount)   <- родитель указывается в скобках

`{profit:F2}` (два знака после запятой) в Python пишется как f"{profit:.2f}".
"""
from banking_system.enums import Currency
from banking_system.exceptions import InvalidOperationError
from banking_system.models.bank_account import BankAccount
from banking_system.utils import to_decimal


class SavingAccount(BankAccount):

    def __init__(self, owner_name: str, currency: Currency, monthly_interest_rate,
                 min_balance=0, initial_balance=0, account_id: str | None = None) -> None:
        # В C# конструктор базового класса (: base(...)) вызывается ПЕРЕД телом.
        # В Python мы сами решаем, когда вызвать super().__init__ — делаем это первым.
        super().__init__(owner_name, currency, initial_balance, account_id)

        monthly_interest_rate = to_decimal(monthly_interest_rate)
        min_balance = to_decimal(min_balance)
        initial_balance = to_decimal(initial_balance)

        if monthly_interest_rate < 0:
            raise InvalidOperationError("Процентная ставка не может быть отрицательной")
        if min_balance < 0:
            raise InvalidOperationError("Минимальный баланс не может быть отрицательным")
        if initial_balance < min_balance:
            raise InvalidOperationError(f"Начальный баланс не может быть меньше минимального ({min_balance})")

        self._min_balance = min_balance
        self._monthly_interest_rate = monthly_interest_rate

    @property
    def min_balance(self):
        return self._min_balance

    @property
    def monthly_interest_rate(self):
        return self._monthly_interest_rate

    # C#: public override void Withdraw(...)
    # В Python слово override не нужно: метод с тем же именем просто заменяет родительский.
    def withdraw(self, amount) -> None:
        amount = to_decimal(amount)
        self._validate_amount(amount)
        self._validate_account_status_for_operation()

        new_balance = self.get_balance() - amount
        if new_balance < self._min_balance:
            raise InvalidOperationError(
                f"Снятие невозможно: баланс не может быть меньше минимального "
                f"({self._min_balance} {self._currency})")

        self._balance -= amount
        print(f"Счет {self._id}: успешно снято {amount} {self._currency}. "
              f"Новый баланс: {self._balance} {self._currency}")

    def calculate_monthly_profit(self):
        return self.get_balance() * (self._monthly_interest_rate / 100)

    def apply_monthly_interest(self) -> None:
        self._validate_account_status_for_operation()
        profit = self.calculate_monthly_profit()
        if profit > 0:
            self._balance += profit
            print(f"Счет {self._id}: начислены проценты {profit:.2f} {self._currency} "
                  f"(ставка {self._monthly_interest_rate}%). Новый баланс: {self._balance} {self._currency}")

    def get_account_info(self) -> str:
        projected_profit = self.calculate_monthly_profit()
        return (f"Информация о сберегательном счете:\n"
                f"Тип счета: {type(self).__name__}\n"
                f"Владелец: {self._owner_name}\n"
                f"Номер счета: ****{self._last_four_digits()}\n"
                f"Полный номер: {self._id}\n"
                f"Статус: {self._status}\n"
                f"Баланс: {self.get_balance()} {self._currency}\n"
                f"Минимальный баланс: {self._min_balance} {self._currency}\n"
                f"Месячная ставка: {self._monthly_interest_rate}%\n"
                f"Проектированная прибыль за месяц: {projected_profit:.2f} {self._currency}\n"
                f"Валюта: {self._currency}")

    def __str__(self) -> str:
        return (f"{type(self).__name__} - {self._owner_name} (****{self._last_four_digits()}) | "
                f"Статус: {self._status} | Баланс: {self.get_balance()} {self._currency} | "
                f"Мин. баланс: {self._min_balance} | Ставка: {self._monthly_interest_rate}%")
