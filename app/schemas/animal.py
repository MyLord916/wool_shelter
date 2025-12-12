from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class AnimalBase(BaseModel):

    name: str = Field(
        None,
        min_length=3,
        max_length=120,
        description="Кличка животного от 3 до 120 символов",
    )
    description: Optional[str] = Field(None)


class AnimalCreate(AnimalBase):
    pass


class AnimalUpdate(AnimalBase):
    name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=120,
        description="Кличка животного от 3 до 120 символов",
    )
    description: Optional[str] = Field(None)


class AnimalResponse(AnimalBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(gt=0, default=1)
