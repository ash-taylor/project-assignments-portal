"""Pydantic validation models for customer requests and responses"""

from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict, Field, field_validator


class CustomerBase(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=50)
    details: Optional[str] = Field(max_length=100)


class CustomerCreate(CustomerBase):
    @field_validator("name", "details", mode="before")
    def strip(cls, v):  # pylint: disable=no-self-argument
        """On creation, strips any leading or trailing whitespace"""
        if v and isinstance(v, str):
            return v.strip()

    name: str = Field(min_length=3, max_length=50)


class CustomerUpdate(CustomerBase):
    @field_validator("name", "details", mode="before")
    def strip(cls, v):  # pylint: disable=no-self-argument
        """On creation, strips any leading or trailing whitespace"""
        if v and isinstance(v, str):
            return v.strip()


class CustomerOut(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    active: bool
