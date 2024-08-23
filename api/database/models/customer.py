from typing import TYPE_CHECKING, List
from uuid import uuid4
from sqlalchemy import UUID, Boolean, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from .project import Project


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    details: Mapped[str] = mapped_column(Text)
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="customer", cascade="all, delete-orphan"
    )
