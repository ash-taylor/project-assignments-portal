from enum import Enum
from typing import List, Optional
from pydantic import UUID4, BaseModel, ConfigDict, Field, field_validator


class ProjectStatus(str, Enum):
    PENDING = "PENDING"
    DESIGN = "DESIGN"
    BUILD = "BUILD"
    COMPLETE = "COMPLETE"


class ProjectBase(BaseModel):
    name: str = Field(min_length=3, max_length=50, pattern="^[A-Za-z]")
    status: ProjectStatus
    details: Optional[str] = Field(max_length=100)
    customer_id: UUID4


class ProjectCreate(ProjectBase):
    @field_validator("name", mode="before")
    def capitalize(cls, v):  # pylint: disable=no-self-argument
        if v and isinstance(v, str):
            return v.strip().capitalize()


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4


class ProjectWithUsersOut(ProjectOut):
    users: Optional[List["UserOut"]]


from .user import UserOut

ProjectOut.model_rebuild()
