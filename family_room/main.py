from fastapi import FastAPI, Depends, HTTPException
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/family', response_model=schemas.Family)
def create_family(family: schemas.FamilyCreate, db: Session = Depends(get_db)):
    return crud.create_family(db=db, family=family)


@app.get('/family/{family_id}', response_model=schemas.Family)
async def get_family(family_id: int, db: Session = Depends(get_db)):
    db_family = crud.get_family(db=db, family_id=family_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail='Семья не найдена')
    return db_family


@app.post('/users/', response_model=schemas.User)
async def create_user(
        family_id: int,
        user: schemas.UserCreate,
        db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким ником уже существует")
    return crud.create_user_family(db=db, user=user, family_id=family_id)


@app.get('/users/', response_model=List[schemas.User])
async def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return db_user
