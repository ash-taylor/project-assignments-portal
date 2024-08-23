from enum import Enum
from pydantic import BaseModel, Field


class Status(str, Enum):
    PENDING = "PENDING"
    DESIGN = "DESIGN"
    BUILD = "BUILD"
    COMPLETE = "COMPLETE"


class ProjectBase(BaseModel):
    name: str = Field(min_length=5, max_length=30, pattern="^[A-Za-z]")
    status: Status
    details: str
