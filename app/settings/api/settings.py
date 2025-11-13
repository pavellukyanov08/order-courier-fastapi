from pydantic_settings import BaseSettings


class ApiSettings(BaseSettings):
    AUTH_TOKENS_PREFIX = '/auth/tokens'
    ORDERS_PREFIX = '/orders'
    COURIERS_PREFIX = '/couriers'
    USERS_PREFIX = '/users'