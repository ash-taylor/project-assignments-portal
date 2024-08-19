from sqlalchemy import Boolean, Column, Integer, String
from . import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(8), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False, unique=True, index=True)
    active = Column(Boolean, default=True, nullable=False)
    admin = Column(Boolean, default=False, nullable=False)


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(8), nullable=False, unique=True)
    active = Column(Boolean, default=True, nullable=False)
    status = Column(String(), nullable=False, index=True)
