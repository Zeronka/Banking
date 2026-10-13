"""
Собственные исключения банковской системы.

C#:
    public abstract class AccountException : Exception
    {
        protected AccountException(string message) : base(message) { }
    }

В Python все исключения наследуются от Exception, а `: base(message)`
превращается в вызов super().__init__(message).
Текст ошибки (ex.Message в C#) в Python получают через str(ex).
"""


class AccountException(Exception):
    """Базовое исключение для всех ошибок счета (в C# оно abstract)."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class AccountClosedError(AccountException):
    def __init__(self) -> None:
        super().__init__("Операция невозможна: счет закрыт")


class AccountFrozenError(AccountException):
    def __init__(self) -> None:
        super().__init__("Операция невозможна: счет заморожен")


class InsufficientFundsError(AccountException):
    def __init__(self) -> None:
        super().__init__("Недостаточно средств на счете")


class InvalidOperationError(AccountException):
    def __init__(self, message: str) -> None:
        # C#: $"Некорректная операция: {message}"  ->  Python: f"..."
        super().__init__(f"Некорректная операция: {message}")
