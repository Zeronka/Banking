"""
Точка входа (аналог Program.cs).

C#:
    class Program { static void Main(string[] args) { ... } }
Python:
    def main(): ...
    if __name__ == "__main__":
        main()
Последние две строки значат «запусти main(), если файл запущен напрямую
(python main.py), а не импортирован из другого файла».
"""
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

    # Запуск полного тестирования
    run_tests()

    # Дополнительные интерактивные примеры
    run_additional_examples()

    # Console.ReadKey() -> input() (ждём Enter)
    input("\nНажмите Enter для выхода...")


def run_additional_examples() -> None:
    print("\n\n=== ДОПОЛНИТЕЛЬНЫЕ ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===\n")

    # Пример 1: Сравнение всех типов счетов
    print("1. СРАВНЕНИЕ ВСЕХ ТИПОВ СЧЕТОВ:")
    print("--------------------------------")

    base_acc = BankAccount("Базовый Клиент", Currency.RUB, 5000)
    saving_acc = SavingAccount("Сберегатель Клиент", Currency.USD, Decimal("6.0"), 1000, 5000)
    premium_acc = PremiumAccount("Премиум Клиент", Currency.EUR, 10000, 20000, 30, 5000)
    invest_acc = InvestmentAccount("Инвестор Клиент", Currency.USD, 20000)

    # print(obj) автоматически вызывает obj.__str__() — как Console.WriteLine(obj) вызывает ToString()
    print(base_acc)
    print(saving_acc)
    print(premium_acc)
    print(invest_acc)

    # Пример 2: Демонстрация специфических операций
    print("\n2. СПЕЦИФИЧЕСКИЕ ОПЕРАЦИИ:")
    print("--------------------------------")

    print("\n>>> Сберегательный счет:")
    print(f"До начисления: {saving_acc.get_balance()}")
    saving_acc.apply_monthly_interest()
    print(f"После начисления: {saving_acc.get_balance()}")

    print("\n>>> Премиум счет (овердрафт):")
    premium_acc.withdraw(6000)  # Уходит в минус
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

    # Пример 3: Обработка ошибок
    print("\n3. ОБРАБОТКА ОШИБОК:")
    print("--------------------------------")

    # Попытка создать сберегательный счет с нарушением мин. баланса
    try:
        SavingAccount("Ошибка", Currency.RUB, 5, 1000, 500)
    except InvalidOperationError as ex:
        print(f"Ошибка создания: {ex}")

    # Попытка превысить овердрафт
    try:
        test_premium = PremiumAccount("Тест", Currency.RUB, 1000, 5000, 10, 500)
        test_premium.withdraw(2000)  # Превышает овердрафт
    except InsufficientFundsError as ex:
        print(f"Ошибка овердрафта: {ex}")

    print("\n=== ПРИМЕРЫ ЗАВЕРШЕНЫ ===")


if __name__ == "__main__":
    main()
