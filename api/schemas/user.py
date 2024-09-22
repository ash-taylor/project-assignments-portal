"""Pydantic validation models for user requests and responses"""

from enum import Enum
from typing import Optional
from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class Roles(str, Enum):
    MANAGER = "MANAGER"
    ENGINEER = "ENGINEER"


class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=128)
    last_name: str = Field(min_length=1, max_length=128)
    email: EmailStr


class UserCreate(UserBase):
    user_name: str = Field(min_length=8, max_length=8, pattern="^[A-Za-z]")
    role: Roles
    password: str = Field(min_length=8, pattern="^[A-Za-z]")

    @field_validator("user_name", "email", mode="before")
    def to_lowercase(cls, v):  # pylint: disable=no-self-argument
        """On creation, strips any leading or trailing whitespace and ensures string is lowercase"""
        if isinstance(v, str):
            return v.strip().lower()

    @field_validator("first_name", "last_name", mode="before")
    def capitalize(cls, v):  # pylint: disable=no-self-argument
        """On creation, strips any leading or trailing whitespace and capitalizes the string"""
        if isinstance(v, str):
            return v.strip().capitalize()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_name": "JohnDoe",
                    "password": "testPassword",
                    "first_name": "john",
                    "last_name": "Doe",
                    "role": "MANAGER",
                    "email": "john@email.com",
                    "confirm_password": "testPassword",
                }
            ]
        }
    }


class UserUpdate(UserBase):
    pass


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    user_name: str = Field(min_length=8, max_length=8, pattern="^[A-Za-z]")
    id: UUID4
    role: Roles
    admin: bool
    active: bool
    project_id: Optional[UUID4]
