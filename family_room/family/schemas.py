from pydantic import BaseModel


class FamilyBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class FamilyCreate(FamilyBase):
    pass


class FamilyRead(FamilyBase):
    id: int
