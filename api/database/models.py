from sqlalchemy import Boolean, Column, Integer, String
from api.database.database import Base


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
