from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_family(db: Session, family: schemas.FamilyCreate):
    db_family = models.Family(name=family.name)
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family


def get_family(db: Session, family_id: int):
    return db.query(models.Family).filter(models.Family.id == family_id).first()


def create_user_family(db: Session, user: schemas.UserCreate, family_id: int):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        full_name=user.full_name,
        birth_day=user.birth_day,
        username=user.username,
        email=user.email,
        hashed_password=fake_hashed_password,
        family_id=family_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
