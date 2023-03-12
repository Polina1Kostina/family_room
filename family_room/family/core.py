from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from family_room.auth.models import family
from .schemas import FamilyCreate


async def get_family_core(family_id: int, session: AsyncSession):
    query = select(family).where(family.c.id == family_id)
    result = await session.execute(query)
    family_row = result.fetchone()
    if family_row is None:
        raise HTTPException(status_code=400, detail='Семья не найдена')
    return family_row


async def create_family_core(new_family: FamilyCreate, session: AsyncSession):
    stmt = insert(family).values(**new_family.dict())
    await session.execute(stmt)
    await session.commit()
    return stmt
