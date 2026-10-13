from dataclasses import dataclass
from decimal import Decimal

from banking_system.enums import Currency
from banking_system.exceptions import InsufficientFundsError, InvalidOperationError
from banking_system.models.bank_account import BankAccount
from banking_system.utils import to_decimal


@dataclass
class InvestmentAsset:
    name: str
    asset_type: str
    quantity: Decimal
    current_price: Decimal
    annual_yield_percent: Decimal

    def __post_init__(self) -> None:
        self.quantity = to_decimal(self.quantity)
        self.current_price = to_decimal(self.current_price)
        self.annual_yield_percent = to_decimal(self.annual_yield_percent)

    def get_value(self) -> Decimal:
        return self.quantity * self.current_price

    def get_yearly_income(self) -> Decimal:
        return self.get_value() * (self.annual_yield_percent / 100)

    def __str__(self) -> str:
        return (f"{self.name} ({self.asset_type}): {self.quantity} шт. по {self.current_price} = "
                f"{self.get_value()} | Доходность: {self.annual_yield_percent}%")


class InvestmentAccount(BankAccount):

    def __init__(self, owner_name: str, currency: Currency, initial_balance=0,
                 account_id: str | None = None) -> None:
        super().__init__(owner_name, currency, initial_balance, account_id)
        self._portfolio: list[InvestmentAsset] = []
        self._investment_balance = Decimal("0")

    @property
    def portfolio(self) -> list[InvestmentAsset]:
        return self._portfolio

    @property
    def investment_balance(self) -> Decimal:
        return self._investment_balance

    @property
    def total_portfolio_value(self) -> Decimal:
        return sum((a.get_value() for a in self._portfolio), Decimal("0"))

    def _find_asset(self, asset_name: str) -> InvestmentAsset | None:
        return next((a for a in self._portfolio if a.name == asset_name), None)

    def transfer_to_investment(self, amount) -> None:
        amount = to_decimal(amount)
        self._validate_amount(amount)
        self._validate_account_status_for_operation()

        if self.get_balance() < amount:
            raise InsufficientFundsError()

        self._balance -= amount
        self._investment_balance += amount
        print(f"Счет {self._id}: переведено {amount} {self._currency} на инвестиционный баланс. "
              f"Основной баланс: {self._balance} {self._currency}")

    def transfer_from_investment(self, amount) -> None:
        amount = to_decimal(amount)
        self._validate_amount(amount)
        self._validate_account_status_for_operation()

        if self._investment_balance < amount:
            raise InvalidOperationError("Недостаточно средств на инвестиционном балансе")

        self._investment_balance -= amount
        self._balance += amount
        print(f"Счет {self._id}: выведено {amount} {self._currency} с инвестиционного баланса. "
              f"Основной баланс: {self._balance} {self._currency}")

    def buy_asset(self, asset: InvestmentAsset) -> None:
        self._validate_account_status_for_operation()

        cost = asset.get_value()
        if self._investment_balance < cost:
            raise InvalidOperationError(
                f"Недостаточно средств для покупки. Требуется: {cost} {self._currency}, "
                f"доступно: {self._investment_balance} {self._currency}")

        self._investment_balance -= cost
        self._portfolio.append(asset)
        print(f"Счет {self._id}: куплен актив {asset.name} на сумму {cost} {self._currency}")

    def sell_asset(self, asset_name: str, quantity) -> None:
        quantity = to_decimal(quantity)
        self._validate_account_status_for_operation()

        asset = self._find_asset(asset_name)
        if asset is None:
            raise InvalidOperationError(f"Актив {asset_name} не найден в портфеле")

        if asset.quantity < quantity:
            raise InvalidOperationError(f"Недостаточно актива для продажи. Доступно: {asset.quantity}")

        sale_value = quantity * asset.current_price
        self._investment_balance += sale_value
        asset.quantity -= quantity

        if asset.quantity == 0:
            self._portfolio.remove(asset)

        print(f"Счет {self._id}: продано {quantity} {asset_name} на сумму {sale_value} {self._currency}")

    def update_asset_price(self, asset_name: str, new_price) -> None:
        asset = self._find_asset(asset_name)
        if asset is not None:
            asset.current_price = to_decimal(new_price)
            print(f"Обновлена цена {asset_name}: {asset.current_price} {self._currency}")

    def project_yearly_growth(self) -> Decimal:
        return sum((a.get_yearly_income() for a in self._portfolio), Decimal("0"))

    def project_portfolio_value_in_year(self) -> Decimal:
        return self.total_portfolio_value + self.project_yearly_growth()

    def withdraw(self, amount) -> None:
        amount = to_decimal(amount)
        self._validate_amount(amount)
        self._validate_account_status_for_operation()

        if self.get_balance() < amount:
            raise InsufficientFundsError()

        self._balance -= amount
        print(f"Счет {self._id}: успешно снято {amount} {self._currency}. "
              f"Новый баланс: {self._balance} {self._currency}")

    def get_portfolio_report(self) -> str:
        lines = ["=== ИНВЕСТИЦИОННЫЙ ПОРТФЕЛЬ ==="]

        if len(self._portfolio) == 0:
            lines.append("Портфель пуст")
        else:
            for asset in self._portfolio:
                lines.append(f"  • {asset}")
            lines.append(f"\nОбщая стоимость портфеля: {self.total_portfolio_value} {self._currency}")
            lines.append(f"Проектированная годовая доходность: {self.project_yearly_growth()} {self._currency}")

        lines.append(f"Свободный инвестиционный баланс: {self._investment_balance} {self._currency}")
        return "\n".join(lines) + "\n"

    def get_account_info(self) -> str:
        main_balance = self.get_balance()
        projected_growth = self.project_yearly_growth()
        total_assets = main_balance + self._investment_balance + self.total_portfolio_value

        lines = [
            "Информация об инвестиционном счете:",
            f"Тип счета: {type(self).__name__}",
            f"Владелец: {self._owner_name}",
            f"Номер счета: ****{self._last_four_digits()}",
            f"Полный номер: {self._id}",
            f"Статус: {self._status}",
            f"Основной баланс: {main_balance} {self._currency}",
            f"Инвестиционный баланс: {self._investment_balance} {self._currency}",
            f"Общая стоимость активов: {self.total_portfolio_value} {self._currency}",
            f"Общие активы: {total_assets} {self._currency}",
            f"Количество активов в портфеле: {len(self._portfolio)}",
            f"Проектированная годовая доходность: {projected_growth:.2f} {self._currency}",
            f"Валюта: {self._currency}",
            "\n" + self.get_portfolio_report(),
        ]
        return "\n".join(lines) + "\n"

    def __str__(self) -> str:
        return (f"{type(self).__name__} - {self._owner_name} (****{self._last_four_digits()}) | "
                f"Статус: {self._status} | Основной: {self.get_balance()} {self._currency} | "
                f"Инвестиции: {self._investment_balance} | "
                f"Активы: {self.total_portfolio_value} ({len(self._portfolio)} шт.)")
