from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import mapped_column
from api.schemas.user import Roles
from . import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(8), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    role = mapped_column(Enum(Roles), nullable=False, index=True)
    email = Column(String(30), nullable=False, unique=True, index=True)
    active = Column(Boolean, default=True, nullable=False)
    admin = Column(Boolean, default=False, nullable=False)


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(8), nullable=False, unique=True)
    active = Column(Boolean, default=True, nullable=False)
    status = Column(String(), nullable=False, index=True)
