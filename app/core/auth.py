from datetime import timedelta, datetime
from typing import Optional, Any

from jose import jwt
from passlib.context import CryptContext
import os

from dotenv import load_dotenv
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.user import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable not set")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTAuth:
    def __init__(
        self,
        *,
        secret_key: str = SECRET_KEY,
        algorithm: str = "HS256",
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm

    def generate_access_token(self, *, data: dict[str, Any], expired_at: datetime) -> str:
        to_encode = data.copy()
        to_encode.update({"exp": expired_at})
        encoded_jwt = jwt.encode(claims=to_encode, key=self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    def validate_token(self, *, token: str) -> dict[str, Any]:
        return jwt.decode(
            token=token, key=self._secret_key, algorithms=[self._algorithm]
        )


class PasswordManager:
    @staticmethod
    def get_hashed_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)


class UserManager:
    def __init__(self, *, db: AsyncSessionLocal, username: str) -> None:
        self._db = db
        self._username = username

    async def get_user(self) -> User | None:
        result = await self._db.execute(select(User).where(User.username == self._username))
        return result.scalar_one_or_none()

    async def authenticate_user(self, *, password: str) -> User | None:
        user = await self.get_user()
        if not user or not password_manager.verify_password(password, user.hashed_password):
            return None
        return user


password_manager = PasswordManager()