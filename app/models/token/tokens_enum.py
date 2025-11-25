from enum import StrEnum


class ActionTokenTypeEnum(StrEnum):
    REGISTER = "register"
    RESET_PASSWORD = "reset_password"


class SessionTokenTypeEnum(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


