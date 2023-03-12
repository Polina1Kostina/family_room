from fastapi import APIRouter, Depends, Response, status
from family_room.auth.dependencies import get_current_user, current_user
from family_room.auth.models import User
from .schemas import EventInvite, EventBase, EventRead
from sqlalchemy.ext.asyncio import AsyncSession
from family_room.auth.database import get_async_session


from .core import (get_event_core, create_event_core, delete_event_core,
                   update_event_core, create_event_invite_core)


router = APIRouter(
    prefix='/event',
    tags=['event'],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}}
)


@router.get('/{event_id}', response_model=EventRead)
async def get_event(
        event_id: int,
        session: AsyncSession = Depends(get_async_session)):
    event = await get_event_core(event_id=event_id, session=session)
    return event


@router.post('/', response_model=EventRead)
async def create_event(
        new_event: EventBase,
        session: AsyncSession = Depends(get_async_session),
        cur_user: User = Depends(current_user)):
    await create_event_core(
            new_event=new_event, session=session, cur_user=cur_user)
    return {**new_event.dict(), 'owner': cur_user.id}


@router.delete('/{event_id}')
async def delete_event(
        event_id: int,
        session: AsyncSession = Depends(get_async_session),
        cur_user: User = Depends(current_user)):
    await delete_event_core(
        event_id=event_id, session=session, cur_user=cur_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{event_id}', response_model=EventBase)
async def update_event(
        event_id: int,
        new_event: EventBase,
        session: AsyncSession = Depends(get_async_session),
        cur_user: User = Depends(current_user)):
    await update_event_core(
            event_id=event_id, new_event=new_event,
            session=session, cur_user=cur_user)
    return {**new_event.dict()}


@router.post('/{event_id}/invite', response_model=EventInvite)
async def create_invite(
        event_id: int,
        invited_id: int,
        session: AsyncSession = Depends(get_async_session),
        cur_user: User = Depends(current_user)):
    await create_event_invite_core(
        event_id=event_id, invited_id=invited_id,
        session=session, cur_user=cur_user
    )
    return {
            'event_id': event_id,
            'invited_id': invited_id
        }
