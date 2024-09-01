from typing import List, Optional
import uuid
from sqlalchemy import UUID, Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.schemas.project import ProjectStatus
from api.schemas.user import Roles

from . import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
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
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("project.id", ondelete="SET NULL"), nullable=True
    )
    project: Mapped[Optional["Project"]] = relationship(back_populates="users")

    def __repr__(self):
        return f"""
<User(
    id={self.id},
    user_name={self.user_name},
    hashed_password={self.hashed_password},
    first_name={self.first_name},
    last_name={self.last_name},
    role={self.role},
    email={self.email},
    active={self.active},
    admin={self.admin},
    project_id={self.project_id}
)>"""


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text)
    projects: Mapped[Optional[List["Project"]]] = relationship(
        back_populates="customer", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"""
<Customer(
    id={self.id},
    name={self.name},
    details={self.details},
    active={self.active}
)>"""


class Project(Base):
    __tablename__ = "project"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), nullable=False, index=True
    )
    details: Mapped[Optional[str]] = mapped_column(Text)
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customer.id", ondelete="CASCADE"),
        nullable=False,
    )
    customer: Mapped["Customer"] = relationship(
        back_populates="projects", lazy="joined"
    )
    users: Mapped[List["User"]] = relationship(back_populates="project")

    def __repr__(self):
        return f"""
<Project(
    id={self.id},
    name={self.name},
    active={self.active},
    status={self.status},
    details={self.details},
    customer_id={self.customer_id}
)>"""
