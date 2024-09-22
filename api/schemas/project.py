"""Pydantic validation models for project requests and responses"""

from enum import Enum
from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict, Field, field_validator


class ProjectStatus(str, Enum):
    PENDING = "PENDING"
    DESIGN = "DESIGN"
    BUILD = "BUILD"
    COMPLETE = "COMPLETE"


class ProjectBase(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=50, pattern="^[A-Za-z]")
    status: Optional[ProjectStatus]
    details: Optional[str] = Field(max_length=100)
    customer_id: Optional[UUID4]


class ProjectCreate(ProjectBase):
    @field_validator("name", mode="before")
    def capitalize(cls, v):  # pylint: disable=no-self-argument
        """On creation, strips any leading or trailing whitespace and capitalizes the string"""
        if v and isinstance(v, str):
            return v.strip().capitalize()

    name: str = Field(min_length=3, max_length=50, pattern="^[A-Za-z]")
    status: ProjectStatus
    details: Optional[str] = Field(max_length=100)
    customer_id: UUID4


class ProjectUpdate(ProjectBase):
    @field_validator("name", mode="before")
    def capitalize(cls, v):  # pylint: disable=no-self-argument
        """On creation, strips any leading or trailing whitespace and capitalizes the string"""
        if v and isinstance(v, str):
            return v.strip().capitalize()

    @field_validator("details", "customer_id", mode="before")
    def strip(cls, v):  # pylint: disable=no-self-argument
        """On creation, strips any leading or trailing whitespace"""
        if v and isinstance(v, str):
            return v.strip()


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    name: str = Field(min_length=3, max_length=50, pattern="^[A-Za-z]")
    status: ProjectStatus
    details: Optional[str] = Field(max_length=100)
    customer_id: UUID4
