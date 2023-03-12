from sqlalchemy import (Date, Boolean, Column, ForeignKey, Integer, MetaData,
                        String, Table, UniqueConstraint)
from fastapi_users.db import SQLAlchemyBaseUserTable
from .database import Base

metadata = MetaData()

family = Table(
    'family',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, index=True)
)

user = Table(
    "user",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),

    Column('birth_day', Date),
    Column('full_name', String),
    Column('username', String, unique=True),
    Column('family_id', Integer, ForeignKey(family.c.id)),

    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=True, nullable=False),
    Column('is_verified', Boolean, default=True, nullable=False),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)

    birth_day = Column(Date)
    full_name = Column(String)
    username = Column(String, unique=True)
    family_id = Column(Integer, ForeignKey(family.c.id))

    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
