from enum import Enum


class AccountStatus(Enum):
    ACTIVE = "Active"
    FROZEN = "Frozen"
    CLOSED = "Closed"

    def __str__(self) -> str:
        return self.value
