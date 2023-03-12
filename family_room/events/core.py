from fastapi import Depends, HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from family_room.tasks.tasks import send_email_invite_event
from .models import event, event_invited
from family_room.auth.dependencies import current_user
from .schemas import EventBase
from family_room.auth.models import User, user


async def get_event_core(
        event_id: int,
        session: AsyncSession = Depends(current_user)):
    query = select(event).where(event.c.id == event_id)
    result = await session.execute(query)
    event_row = result.fetchone()
    if event_row is None:
        raise HTTPException(
            status_code=400, detail=("Мероприятие не найдено"))
    return event_row


async def create_event_core(
        new_event: EventBase,
        session: AsyncSession,
        cur_user: User):
    try:
        stmt = insert(event).values(**new_event.dict(), owner=cur_user.id)
        await session.execute(stmt)
        await session.commit()
        return stmt
    except Exception:
        return HTTPException(
            status_code=400, detail=("Мероприятие не создано"))


async def verify_event_owner(
        event_id: int,
        session: AsyncSession,
        cur_user: User):
    event_row = await get_event_core(event_id=event_id, session=session)
    if event_row.owner != cur_user.id:
        raise HTTPException(
            status_code=400, detail=("Вы не являетесь владельцем мероприятия"))
    return event_row


async def delete_event_core(
        event_id: int,
        session: AsyncSession,
        cur_user: User):
    await verify_event_owner(
        event_id=event_id, session=session, cur_user=cur_user)
    try:
        stmt = delete(event).where(event.c.id == event_id)
        await session.execute(stmt)
        await session.commit()
        return stmt
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail=("Мероприятие не удалось удалить"))


async def update_event_core(
        event_id: int,
        new_event: EventBase,
        session: AsyncSession,
        cur_user: User):
    await verify_event_owner(
        event_id=event_id, session=session, cur_user=cur_user)
    try:
        stmt = update(event).where(
            event.c.id == event_id).values(**new_event.dict())
        await session.execute(stmt)
        await session.commit()
    except Exception:
        raise HTTPException(
            status_code=400, detail=("Мероприятие не удалось изменить"))


async def create_event_invite_core(
        event_id: int,
        invited_id: int,
        session: AsyncSession,
        cur_user: User):
    event_row = await verify_event_owner(
        event_id=event_id, session=session, cur_user=cur_user)
    result = await session.execute(select(user).where(user.c.id == invited_id))
    invited_row = result.fetchone()
    if invited_row is None:
        raise HTTPException(
            status_code=400, detail=("Такой пользователь не найден"))
    try:
        stmt = insert(event_invited).values(
            event_id=event_id, invited_id=invited_id)
        await session.execute(stmt)
        await session.commit()
        send_email_invite_event.delay(invited_row.email, event_row.title)
    except Exception:
        raise HTTPException(
            status_code=400, detail=(
                "Не удалось обработать запрос, "
                "возможно приглашение уже было создано"))
