"""
Абстрактный базовый счет.

Главные отличия от C#:
  * `abstract class`         ->  наследование от ABC + декоратор @abstractmethod
  * конструктор `AbstractAccount(...)`  ->  метод __init__(self, ...)
  * `this`                   ->  self (в Python его пишут явно первым параметром)
  * `public string Id { get; protected set; }`
        -> атрибут self._id + @property id (только чтение снаружи)
  * `protected`              ->  имя с одним подчёркиванием: self._balance
        (это соглашение: Python не запрещает доступ, но «снаружи не трогать»)
  * `override ToString()`    ->  __str__(self)
  * `GetType().Name`         ->  type(self).__name__
"""
from abc import ABC, abstractmethod
from decimal import Decimal

from banking_system.enums import AccountStatus


class AbstractAccount(ABC):

    def __init__(self, account_id: str, owner_name: str, initial_balance: Decimal = Decimal("0")) -> None:
        self._id = account_id
        self._owner_name = owner_name
        self._balance = initial_balance          # protected decimal Balance
        self._status = AccountStatus.ACTIVE

    # ---------- свойства (properties) только для чтения ----------
    @property
    def id(self) -> str:
        return self._id

    @property
    def owner_name(self) -> str:
        return self._owner_name

    @property
    def status(self) -> AccountStatus:
        return self._status

    # ---------- абстрактные методы ----------
    # Наследник ОБЯЗАН их реализовать, иначе создать объект не получится.
    @abstractmethod
    def deposit(self, amount) -> None: ...

    @abstractmethod
    def withdraw(self, amount) -> None: ...

    @abstractmethod
    def get_account_info(self) -> str: ...

    # В C# эта строчка повторялась в каждом классе:
    #   Id.Length >= 4 ? Id.Substring(Id.Length - 4) : Id
    # В Python срез строки s[-4:] делает то же самое (последние 4 символа),
    # поэтому вынесли в один маленький метод.
    def _last_four_digits(self) -> str:
        return self._id[-4:]

    def __str__(self) -> str:
        return (f"Тип: {type(self).__name__}, Клиент: {self._owner_name}, "
                f"Номер: ****{self._last_four_digits()}, "
                f"Статус: {self._status}, Баланс: {self._balance}")
