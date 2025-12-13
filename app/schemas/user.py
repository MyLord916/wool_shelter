from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


class UserBase(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=120,
        description="Имя пользователя от 3 до 120 символов",
    )
    is_admin: bool = Field(default=False)

    @field_validator("username", mode="before")
    def validate_name(cls, v):
        if isinstance(v, int):
            return str(v)
        elif isinstance(v, str):
            return v
        else:
            raise ValueError("Имя должно быть строкой или числом")


class UserCreate(UserBase):

    password: str = Field(
        min_length=6,
        repr=False,
        description="Пароль должен содержать минимум 6 символов",
    )


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0, default=1)


class UserUpdate(BaseModel):

    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=120,
        description="Имя пользователя от 3 до 120 символов",
    )

    password: Optional[str] = Field(None, min_length=6)
    is_admin: Optional[bool] = Field(None)

    @field_validator("username", mode="before")
    def validate_name(cls, v):
        if isinstance(v, int):
            return str(v)
        elif isinstance(v, str):
            return v
        else:
            raise ValueError("Имя должно быть строкой или числом")


class UserLogin(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
