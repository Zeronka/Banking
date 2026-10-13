"""
Демонстрационные «тесты» всех типов счетов.

C#: public static class BankAccountTester { public static void RunTests() ... }
В Python статический класс не нужен: функции можно класть прямо в модуль (файл).

  * try { } catch (AccountFrozenError ex) { }  ->  try: ... except AccountFrozenError as ex: ...
  * ex.Message                                 ->  ex (f-строка сама вызовет str(ex))
  * catch (Exception ex)                       ->  except Exception as ex
  * литерал decimal 5.5m                       ->  Decimal("5.5")
"""
from decimal import Decimal

from banking_system.enums import Currency
from banking_system.exceptions import (
    AccountFrozenError,
    InsufficientFundsError,
    InvalidOperationError,
)
from banking_system.models import (
    BankAccount,
    InvestmentAccount,
    InvestmentAsset,
    PremiumAccount,
    SavingAccount,
)


def run_tests() -> None:
    print("=== ТЕСТИРОВАНИЕ БАНКОВСКОЙ СИСТЕМЫ ===\n")

    test_base_account()
    test_saving_account()
    test_premium_account()
    test_investment_account()

    print("\n=== ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ ===")


def test_base_account() -> None:
    print("\n>>> ТЕСТИРОВАНИЕ БАЗОВОГО СЧЕТА <<<\n")

    try:
        account = BankAccount("Иван Иванов", Currency.RUB, 1000)
        print(account.get_account_info())
        print()

        account.deposit(500)
        account.withdraw(300)
        account.freeze_account()

        try:
            account.withdraw(100)
        except AccountFrozenError as ex:
            print(f"Ожидаемая ошибка: {ex}")

        account.unfreeze_account()
        account.withdraw(100)
        print(f"Итоговый баланс: {account.get_balance()}")
    except Exception as ex:
        print(f"Ошибка: {ex}")


def test_saving_account() -> None:
    print("\n>>> ТЕСТИРОВАНИЕ СБЕРЕГАТЕЛЬНОГО СЧЕТА <<<\n")

    try:
        # Создание с минимальным балансом 500 и ставкой 5.5%
        saving = SavingAccount("Петр Сидоров", Currency.USD, Decimal("5.5"), 500, 1000)
        print(saving.get_account_info())
        print()

        # Попытка снять больше, чем позволяет мин. баланс
        print("Попытка снять 600 (мин. баланс 500):")
        try:
            saving.withdraw(600)
        except InvalidOperationError as ex:
            print(f"Ожидаемая ошибка: {ex}")

        # Успешное снятие
        print("\nСнятие 400 (должно работать):")
        saving.withdraw(400)
        print(f"Баланс: {saving.get_balance()}, Минимум: {saving.min_balance}")

        # Расчет прибыли
        print(f"\nПрибыль за месяц: {saving.calculate_monthly_profit():.2f} {saving.currency}")

        # Начисление процентов
        saving.apply_monthly_interest()
        print(f"Баланс после начисления: {saving.get_balance()}")

        print("\n" + str(saving))
    except Exception as ex:
        print(f"Ошибка: {ex}")


def test_premium_account() -> None:
    print("\n>>> ТЕСТИРОВАНИЕ ПРЕМИУМ СЧЕТА <<<\n")

    try:
        # Создание с овердрафтом 5000, лимитом 10000, комиссией 50
        premium = PremiumAccount("Олег Премьер", Currency.EUR, 5000, 10000, 50, 1000)
        print(premium.get_account_info())
        print()

        print("Снятие 800:")
        premium.withdraw(800)
        print()

        print("Снятие 500 (должно уйти в овердрафт):")
        premium.withdraw(500)
        print(f"Доступно овердрафта: {premium.get_available_overdraft()}")
        print()

        print("Попытка снять 5000 (превышение овердрафта):")
        try:
            premium.withdraw(5000)
        except InsufficientFundsError as ex:
            print(f"Ожидаемая ошибка: {ex}")

        print("\nПополнение на 2000:")
        premium.deposit(2000)
        print(premium)
    except Exception as ex:
        print(f"Ошибка: {ex}")


def test_investment_account() -> None:
    print("\n>>> ТЕСТИРОВАНИЕ ИНВЕСТИЦИОННОГО СЧЕТА <<<\n")

    try:
        invest = InvestmentAccount("Анна Инвестор", Currency.USD, 10000)
        print(invest.get_account_info())
        print()

        print("Перевод 5000 на инвестиционный баланс:")
        invest.transfer_to_investment(5000)
        print(f"Основной баланс: {invest.get_balance()}, Инвестиционный: {invest.investment_balance}")
        print()

        print("Покупка активов:")
        apple_stock = InvestmentAsset(
            name="AAPL",
            asset_type="Stocks",
            quantity=10,
            current_price=150,
            annual_yield_percent=Decimal("8.5"),
        )
        invest.buy_asset(apple_stock)

        bond = InvestmentAsset(
            name="US Treasury 10Y",
            asset_type="Bonds",
            quantity=5,
            current_price=1000,
            annual_yield_percent=Decimal("4.2"),
        )
        invest.buy_asset(bond)

        print(invest.get_portfolio_report())
        print()

        print(f"Проектированная годовая доходность: {invest.project_yearly_growth():.2f} {invest.currency}")
        print(f"Стоимость портфеля через год: {invest.project_portfolio_value_in_year():.2f} {invest.currency}")
        print()

        print("Продажа 5 акций AAPL:")
        invest.sell_asset("AAPL", 5)
        print(invest)
    except Exception as ex:
        print(f"Ошибка: {ex}")
