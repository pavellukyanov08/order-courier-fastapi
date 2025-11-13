import logging
from typing import Annotated
from fastapi import Depends, Request
from app.core import JWTAuth
from redis import Redis

from app.api.tokens.services import TokenService
from app.api.tokens.adapters.storage import RedisTokenAdapter


def _get_redis_client(request: Request) -> Redis:
    redis_client: Redis | None = getattr(
        request.state, "redis_client", None
    )
    if not redis_client:
        raise RuntimeError("Missing required request state: redis_client")
    return redis_client

def _get_token_storage_adapter(
    logger: logging.Logger,
    redis_client: Annotated[Redis, Depends(_get_redis_client)],
) -> RedisTokenAdapter:
    return RedisTokenAdapter(
        logger=logger,
        redis_client=redis_client,
    )

def _get_jwt_auth(request: Request) -> JWTAuth:
    jwt_auth: JWTAuth | None = getattr(request, "jwt_auth", None)
    if not jwt_auth:
        raise RuntimeError("Missing required request state: jwt_auth")
    return jwt_auth

def _get_token_service(
    request: Request,
    logger: logging.Logger,
    jwt_auth: Annotated[JWTAuth, Depends(_get_jwt_auth)],
    storage_adapter: Annotated[RedisTokenAdapter, Depends(_get_token_storage_adapter)],
) -> TokenService:
    return TokenService(
        request=request,
        logger=logger,
        jwt_auth=jwt_auth,
        storage_adapter=storage_adapter,
    )

def _get_token_service(
    request: Request,
    logger: logging.Logger,
    jwt_auth: Annotated[JWTAuth, Depends(_get_jwt_auth)],
    storage_adapter: Annotated[RedisTokenAdapter, Depends(_get_token_storage_adapter)],
) -> TokenService:
    return TokenService(
        request=request,
        logger=logger,
        jwt_auth=jwt_auth,
        storage_adapter=storage_adapter,
    )


def _get_token_service(
    request: Request,
    logger: logging.Logger,
    jwt_auth: Annotated[JWTAuth, Depends(_get_jwt_auth)],
    storage_adapter: Annotated[RedisTokenAdapter, Depends(_get_token_storage_adapter)],
) -> TokenService:
    return TokenService(
        request=request,
        logger=logger,
        jwt_auth=jwt_auth,
        storage_adapter=storage_adapter,
    )


TokenServiceDep = Annotated[TokenService, Depends(_get_token_service)]
