from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    user_name: str
    first_name: str
    last_name: str
    email: EmailStr
    active: bool
    admin: bool


class UserCreate(UserBase):
    password: str
