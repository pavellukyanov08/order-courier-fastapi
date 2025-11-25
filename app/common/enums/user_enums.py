from enum import Enum, unique


@unique
class UserRoleEnum(str, Enum):
    Courier: str = "Курьер"
