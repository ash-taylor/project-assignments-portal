from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict, Field, field_validator


class CustomerBase(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    details: Optional[str] = Field(max_length=100)


class CustomerCreate(CustomerBase):
    @field_validator("name", mode="before")
    def capitalize(cls, v):  # pylint: disable=no-self-argument
        if v and isinstance(v, str):
            return v.strip().capitalize()


class CustomerOut(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    active: bool
