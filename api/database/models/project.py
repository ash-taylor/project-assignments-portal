from sqlalchemy import UUID, Boolean, Column, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Project(Base):
    __tablename__ = "project"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        server_default=text("gen_random_uuid()"),
    )
    project_name = Column(String(8), nullable=False, unique=True)
    active = Column(Boolean, default=True, nullable=False)
    status = Column(String(), nullable=False, index=True)
    details: Mapped[str] = mapped_column(Text)
