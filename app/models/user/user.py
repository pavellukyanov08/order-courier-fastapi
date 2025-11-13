from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from ..courier import Courier


class User(Base):
    __tablename__ = "users"

    sid: Mapped[UUID] = mapped_column(
        unique=True, primary_key=True, index=True, default=uuid4
    )
    email: Mapped[str] = mapped_column(
        index=True, unique=True, comment="Email of user"
    )
    username: Mapped[str] = mapped_column(nique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(
        comment="Hashed password of user"
    )

    courier: Mapped["Courier"] = relationship(
            back_populates="user"
    )
