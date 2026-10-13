class AccountException(Exception):

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
        super().__init__(f"Некорректная операция: {message}")
