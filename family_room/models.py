from sqlalchemy import Date, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Family(Base):
    __tablename__ = "family"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    users = relationship("User", back_populates="family")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    birth_day = Column(Date)
    full_name = Column(String)
    username = Column(String, unique=True)
    family_id = Column(Integer, ForeignKey('family.id'))

    family = relationship("Family", back_populates="users")
