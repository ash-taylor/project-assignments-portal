from enum import Enum
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProjectStatus(str, Enum):
    PENDING = "PENDING"
    DESIGN = "DESIGN"
    BUILD = "BUILD"
    COMPLETE = "COMPLETE"


class ProjectBase(BaseModel):
    name: str = Field(min_length=3, max_length=50, pattern="^[A-Za-z]")
    status: ProjectStatus
    details: Optional[str] = Field(max_length=100)


class ProjectCreate(ProjectBase):
    @field_validator("name", mode="before")
    def capitalize(cls, v):  # pylint: disable=no-self-argument
        if v and isinstance(v, str):
            return v.strip().capitalize()


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    users: "Optional[List[UserOut]]"  # Forward reference


from .user import UserOut

ProjectOut.model_rebuild()
