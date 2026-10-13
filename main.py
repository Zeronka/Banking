from decimal import Decimal

from banking_system.enums import Currency
from banking_system.exceptions import InsufficientFundsError, InvalidOperationError
from banking_system.models import (
    BankAccount,
    InvestmentAccount,
    InvestmentAsset,
    PremiumAccount,
    SavingAccount,
)
from banking_system.services import run_tests


def main() -> None:
    print("=== МОДУЛЬНАЯ БАНКОВСКАЯ СИСТЕМА ===\n")

    run_tests()

    run_additional_examples()

    input("\nНажмите Enter для выхода...")


def run_additional_examples() -> None:
    print("\n\n=== ДОПОЛНИТЕЛЬНЫЕ ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===\n")

    print("1. СРАВНЕНИЕ ВСЕХ ТИПОВ СЧЕТОВ:")
    print("--------------------------------")

    base_acc = BankAccount("Базовый Клиент", Currency.RUB, 5000)
    saving_acc = SavingAccount("Сберегатель Клиент", Currency.USD, Decimal("6.0"), 1000, 5000)
    premium_acc = PremiumAccount("Премиум Клиент", Currency.EUR, 10000, 20000, 30, 5000)
    invest_acc = InvestmentAccount("Инвестор Клиент", Currency.USD, 20000)

    print(base_acc)
    print(saving_acc)
    print(premium_acc)
    print(invest_acc)

    print("\n2. СПЕЦИФИЧЕСКИЕ ОПЕРАЦИИ:")
    print("--------------------------------")

    print("\n>>> Сберегательный счет:")
    print(f"До начисления: {saving_acc.get_balance()}")
    saving_acc.apply_monthly_interest()
    print(f"После начисления: {saving_acc.get_balance()}")

    print("\n>>> Премиум счет (овердрафт):")
    premium_acc.withdraw(6000)
    print(premium_acc)

    print("\n>>> Инвестиционный счет:")
    invest_acc.transfer_to_investment(15000)

    etf = InvestmentAsset(name="SPY", asset_type="ETF", quantity=20,
                          current_price=450, annual_yield_percent=Decimal("10.0"))
    crypto = InvestmentAsset(name="BTC", asset_type="Crypto", quantity=Decimal("0.5"),
                             current_price=50000, annual_yield_percent=Decimal("25.0"))

    invest_acc.buy_asset(etf)
    invest_acc.buy_asset(crypto)

    print(invest_acc.get_portfolio_report())
    print(f"Общая проектированная доходность: {invest_acc.project_yearly_growth():.2f} USD")

    print("\n3. ОБРАБОТКА ОШИБОК:")
    print("--------------------------------")

    try:
        SavingAccount("Ошибка", Currency.RUB, 5, 1000, 500)
    except InvalidOperationError as ex:
        print(f"Ошибка создания: {ex}")

    try:
        test_premium = PremiumAccount("Тест", Currency.RUB, 1000, 5000, 10, 500)
        test_premium.withdraw(2000)
    except InsufficientFundsError as ex:
        print(f"Ошибка овердрафта: {ex}")

    print("\n=== ПРИМЕРЫ ЗАВЕРШЕНЫ ===")


if __name__ == "__main__":
    main()
