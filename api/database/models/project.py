from typing import TYPE_CHECKING, List
from uuid import uuid4
from sqlalchemy import UUID, Boolean, Column, ForeignKey, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from .customer import Customer
    from .user import User


class Project(Base):
    __tablename__ = "project"

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
    status = Column(String(), nullable=False, index=True)
    details: Mapped[str] = mapped_column(Text)
    customer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customer.id", ondelete="CASCADE"),
        nullable=False,
    )
    customer: Mapped["Customer"] = relationship("Customer", back_populates="projects")
    users: Mapped[List["User"]] = relationship("User", back_populates="project")
