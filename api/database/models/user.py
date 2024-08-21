from sqlalchemy import UUID, Boolean, Enum, String, text
from sqlalchemy.orm import Mapped, mapped_column
from api.schemas.user import Roles

from . import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        server_default=text("gen_random_uuid()"),
    )
    user_name: Mapped[str] = mapped_column(String(8), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    role: Mapped[Roles] = mapped_column(Enum(Roles), nullable=False, index=True)
    email: Mapped[str] = mapped_column(
        String(30), nullable=False, unique=True, index=True
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
