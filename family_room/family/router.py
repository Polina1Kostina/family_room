from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from family_room.auth.dependencies import get_current_user
from .schemas import FamilyCreate, FamilyRead, FamilyBase
from family_room.auth.database import get_async_session
from .core import get_family_core, create_family_core

router = APIRouter(
    prefix='/family',
    tags=['family'],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}}
)


@router.get('/{family_id}', response_model=FamilyRead)
async def get_family(
        family_id: int,
        session: AsyncSession = Depends(get_async_session)):
    family = await get_family_core(family_id=family_id, session=session)
    return family


@router.post('/', response_model=FamilyBase)
async def create_family(
        new_family: FamilyCreate,
        session: AsyncSession = Depends(get_async_session)):
    await create_family_core(new_family=new_family, session=session)
    return {**new_family.dict()}
