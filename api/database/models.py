from typing import List
from uuid import uuid4
from sqlalchemy import UUID, Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.schemas.project import ProjectStatus
from api.schemas.user import Roles

from . import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
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


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    details: Mapped[str] = mapped_column(Text)
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="customer", cascade="all, delete-orphan"
    )


class Project(Base):
    __tablename__ = "project"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), nullable=False, index=True
    )
    details: Mapped[str] = mapped_column(Text)
    customer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customer.id", ondelete="CASCADE"),
        nullable=False,
    )
    customer: Mapped["Customer"] = relationship("Customer", back_populates="projects")
    users: Mapped[List["User"]] = relationship("User", back_populates="project")
