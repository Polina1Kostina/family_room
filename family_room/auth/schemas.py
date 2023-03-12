from pydantic import EmailStr, Field
from typing import Optional
import datetime
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    family_id: int = None
    id: int
    full_name: str = Field(title="имя и фамилия", max_length=200)
    birth_day: datetime.date = Field(title="Дата рождения",)
    username: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    username: str
    password: str
    full_name: str = Field(title="имя и фамилия", max_length=200)
    birth_day: datetime.date = Field(title="Дата рождения",)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    family_id: int = None
