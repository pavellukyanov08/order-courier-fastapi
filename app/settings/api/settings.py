from pydantic_settings import BaseSettings


class ApiSettings(BaseSettings):
    AUTH_TOKENS_PREFIX: str = '/auth/tokens'
    ORDERS_PREFIX: str = '/orders'
    COURIERS_PREFIX: str = '/couriers'
    USERS_PREFIX: str = '/users'


api_settings = ApiSettings()