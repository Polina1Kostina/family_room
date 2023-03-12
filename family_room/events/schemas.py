from pydantic import BaseModel, EmailStr, Field
from typing import List
import datetime


class EventBase(BaseModel):
    title: str
    place: str
    date: datetime.date = Field(title="Дата мероприятия",)
    description: str

    class Config:
        orm_mode = True


class EventCreate(EventBase):
    invited: List[int] = []


class EventRead(EventBase):
    owner: int


class EventInvite(BaseModel):
    event_id: int
    invited_id: int

    class Config:
        orm_mode = True


class Email(BaseModel):
    email: List[EmailStr]
