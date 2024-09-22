"""Pydantic validation models for auth tokens"""

from pydantic import UUID4, BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID4
    username: str
    admin: bool
