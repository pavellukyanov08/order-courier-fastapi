import logging
from datetime import timedelta
from urllib.request import Request
from uuid import UUID, uuid4

from app.core import JWTAuth
from app.utils import CryptoManager, DateTimeManager
from app.schemas.tokens import TokenDataDTO, RefreshTokenPairDTO, RevokeTokenPairDTO, RevokeAllTokensDTO, TokenPairDTO
from app.models.token import SessionTokenTypeEnum
from app.settings.jwt import JwtSettings
from app.models.token import TokenModel
from app.adapters.token import RedisTokenAdapter


class TokenService:
    def __init__(
        self,
        *,
        request: Request,
        logger: logging.Logger,
        storage_adapter: RedisTokenAdapter,
        jwt_auth: JWTAuth,
    ) -> None:
        self._logger = logger
        self._storage_adapter = storage_adapter
        self._jwt_auth = jwt_auth
        self._ip_header = request.headers.get("x-real-ip", None)
        self._proxy_header = request.headers.get("x-proxy-name", None)
        self._location_header = request.headers.get("x-client-location", None)
        self._os_header = request.headers.get("x-client-os", None)
        self._device_header = request.headers.get("x-client-device", None)
        self._source_header = request.headers.get("x-client-source", None)
        self._user_agent_header = request.headers.get("user-agent", None)
        self._token_ttl = {
            SessionTokenTypeEnum.ACCESS: JwtSettings.ACCESS_TOKEN_TTL,
            SessionTokenTypeEnum.REFRESH: JwtSettings.REFRESH_TOKEN_TTL,
        }

    @staticmethod
    def _get_token_hash(
        *,
        token: str
    ) -> str:
        return CryptoManager.get_hash_sha256(data=token)

    @staticmethod
    def _get_fingerprint_hash(
        *,
        fingerprint: str
    ) -> str:
        return CryptoManager.get_hash_sha256(data=fingerprint)

    def _get_token_with_data(
        self,
        *,
        token_owner: UUID,
        token_type: SessionTokenTypeEnum,
    ) -> tuple[str, TokenDataDTO]:
        ttl = self._token_ttl.get(token_type, 0)
        created_at = DateTimeManager.get_now_utc()
        expired_at = created_at + timedelta(seconds=ttl)
        data = TokenDataDTO(
            token_owner=token_owner,
            type=token_type,
            token_id=uuid4(),
            created_at=created_at,
            expired_at=expired_at,
        )
        token = self._jwt_auth.generate_access_token(
            data=data.model_dump(mode="json"),
            expired_at=expired_at,
        )
        return token, data

    def _get_token_model(
        self,
        *,
        token: str,
        token_data: TokenDataDTO,
        fingerprint: str,
    ) -> TokenModel:
        token_hash = self._get_token_hash(token=token)
        return TokenModel(
            sid=token_data.token_id,
            token_owner=token_data.sub,
            type=token_data.type,
            hash=token_hash,
            fingerprint=fingerprint,
            ip=self._ip_header,
            device=self._device_header,
            user_agent=self._user_agent_header,
            expired_at=token_data.expired_at,
            created_at=token_data.created_at,
        )

    def _get_token_with_model(
        self,
        *,
        token_owner: UUID,
        token_type: SessionTokenTypeEnum,
        fingerprint: str,
    ) -> tuple[str, TokenModel]:
        token, token_data = self._get_token_with_data(
            token_owner=token_owner,
            token_type=token_type,
        )
        token_model = self._get_token_model(
            token=token,
            token_data=token_data,
            fingerprint=fingerprint,
        )
        return token, token_model

    def _get_token_data(
        self,
        *,
        token: str,
        token_type: SessionTokenTypeEnum,
    ) -> TokenDataDTO:
        try:
            token_data = self._jwt_auth.validate_token(token=token)
            return TokenDataDTO.model_validate(obj=token_data)
        except Exception as e:
            self._logger.error("Failed receiving token data: error=%s", e)
            raise

    async def get_token(
        self,
        *,
        token_sid: UUID
    ) -> TokenModel | None:
        return await self._storage_adapter.get_token(token_sid=token_sid)

    async def create_token_pair(
        self,
        *,
        access_token: TokenModel,
        refresh_token: TokenModel,
    ) -> None:
        await self._storage_adapter.create_token_pair(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def _validate_token(
        self,
        *,
        token: str,
        token_type: SessionTokenTypeEnum,
    ) -> TokenModel:
        token_data = self._get_token_data(
            token=token, token_type=token_type
        )
        if token_data.type != token_type:
            raise ValueError("Invalid access token")
        token_model = await self.get_token(
            token_sid=token_data.token_id
        )
        if token_model is None or token_model.hash != self._get_token_hash(
            token=token
        ):
            raise ValueError("Invalid access token")

        return token_model


    async def remove_token_pair(
        self,
        *,
        token_owner: UUID,
        fingerprint: str,
    ) -> None:
        await self._storage_adapter.remove_token_pair(
            token_owner=token_owner,
            fingerprint=fingerprint,
        )

    async def remove_all_tokens(
        self,
        *,
        token_owner: UUID,
    ) -> None:
        await self._storage_adapter.remove_all_tokens(
            token_owner=token_owner,
        )

    async def refresh_token_pair(
        self, *, data: RefreshTokenPairDTO
    ) -> TokenPairDTO:
        token_model = await self._validate_token(
            token=data.refresh_token, token_type=SessionTokenTypeEnum.REFRESH
        )
        access_token, access_token_model = self._get_token_with_model(
            token_owner=token_model.token_owner,
            token_type=SessionTokenTypeEnum.ACCESS,
            fingerprint=token_model.fingerprint,
        )
        refresh_token, refresh_token_model = self._get_token_with_model(
            token_owner=token_model.token_owner,
            token_type=SessionTokenTypeEnum.REFRESH,
            fingerprint=token_model.fingerprint,
        )
        await self.remove_token_pair(
            token_owner=token_model.token_owner,
            fingerprint=token_model.fingerprint,
        )
        await self.create_token_pair(
            access_token=access_token_model,
            refresh_token=refresh_token_model,
        )
        return TokenPairDTO(
            access_token=access_token, refresh_token=refresh_token
        )

    async def revoke_token_pair(
        self, *, data: RevokeTokenPairDTO
    ) -> str:
        fingerprint = self._get_fingerprint_hash(
            fingerprint=data.fingerprint
        )
        await self.remove_token_pair(
            token_owner=data.token_owner,
            fingerprint=fingerprint,
        )
        return "OK"

    async def revoke_all_tokens(
        self, *, data: RevokeAllTokensDTO
    ) -> str:
        await self.remove_all_tokens(
            token_owner=data.token_owner,
        )
        return "OK"