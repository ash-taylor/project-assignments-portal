from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class Roles(str, Enum):
    MANAGER = "MANAGER"
    ENGINEER = "ENGINEER"
    CUSTOMER = "CUSTOMER"


class UserBase(BaseModel):
    user_name: str = Field(min_length=8, max_length=8, pattern="^[A-Za-z]")
    first_name: str = Field(min_length=1, max_length=128)
    last_name: str = Field(min_length=1, max_length=128)
    role: Roles
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @field_validator("user_name", "email", mode="before")
    def to_lowercase(cls, v):  # pylint: disable=no-self-argument
        if isinstance(v, str):
            return v.strip().lower()

    @field_validator("first_name", "last_name", mode="before")
    def capitalize(cls, v):  # pylint: disable=no-self-argument
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
                }
            ]
        }
    }


class UserHashed(UserBase):
    hashed_password: str


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    active: bool
    admin: bool
