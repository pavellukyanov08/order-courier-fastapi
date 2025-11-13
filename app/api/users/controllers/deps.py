import logging
from typing import Annotated
from fastapi import Depends, Request
from app.core import JWTAuth
from redis import Redis

from app.api.tokens.services import TokenService
from app.api.tokens.adapters.storage import RedisTokenAdapter

def _get_jwt_auth(request: Request) -> JWTAuth:
    jwt_auth: JWTAuth | None = getattr(request, "jwt_auth", None)
    if not jwt_auth:
        raise RuntimeError("Missing required request state: jwt_auth")
    return jwt_auth

def _get_user_service(
    logger: logging.Logger,
) -> TokenService:
    return TokenService(
        request=request,
        logger=logger,
        jwt_auth=jwt_auth,
        storage_adapter=storage_adapter,
    )

TokenServiceDep = Annotated[TokenService, Depends(_get_token_service)]
