from pydantic import BaseModel, Field
from typing import Union, List
import datetime


class UserBase(BaseModel):
    full_name: str = Field(title="имя и фамилия", max_length=200)
    birth_day: datetime.date = Field(title="Дата рождения",)
    username: str
    disabled: Union[bool, None] = None
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    family_id: int

    class Config:
        orm_mode = True


class FamilyBase(BaseModel):
    name: str


class FamilyCreate(FamilyBase):
    pass


class Family(FamilyBase):
    id: int
    users: List[User] = []

    class Config:
        orm_mode = True


class Parents(BaseModel):
    mom: Union[User, None] = Field(default=None, title="Мама")
    dad: Union[User, None] = Field(default=None, title="Папа")
    user: User
