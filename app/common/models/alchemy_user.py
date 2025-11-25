from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.common.enums import UserRoleEnum
from app.utils import DateTimeManager


class User(Base):
    __tablename__ = "user"

    sid: Mapped[UUID] = mapped_column(
        unique=True, primary_key=True, index=True, default=uuid4
    )
    email: Mapped[str] = mapped_column(String(length=100), index=True, unique=True, comment="Email of user")
    username: Mapped[str] = mapped_column(index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(
        comment="Hashed password of user"
    )
    role: Mapped[UserRoleEnum] = mapped_column(comment="Role of user")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
        default=DateTimeManager.get_now_utc,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=DateTimeManager.get_now_utc,
        onupdate=DateTimeManager.get_now_utc,
    )

    courier = relationship(
        "Courier",
        back_populates="user",
        cascade="all, delete-orphan",
    )
