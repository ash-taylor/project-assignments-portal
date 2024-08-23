from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import UUID, Boolean, Enum, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.schemas.user import Roles

from . import Base

if TYPE_CHECKING:
    from .project import Project


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
    user_name: Mapped[str] = mapped_column(
        String(8), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    role: Mapped[Roles] = mapped_column(Enum(Roles), nullable=False, index=True)
    email: Mapped[str] = mapped_column(
        String(30), nullable=False, unique=True, index=True
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    project_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("project.id", ondelete="SET NULL"), nullable=True
    )
    project: Mapped["Project"] = relationship("Project", back_populates="users")
