from sqlalchemy import (MetaData, Table, Date, Column, ForeignKey, Integer,
                        String, UniqueConstraint)

from family_room.auth.models import user


metadata = MetaData()

event = Table(
    'event',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('owner', Integer, ForeignKey(user.c.id, ondelete='CASCADE')),
    Column('title', String, index=True),
    Column('place', String),
    Column('date', Date),
    Column('description', String)
)

event_invited = Table(
    'event_invited',
    metadata,
    Column('event_id', Integer, ForeignKey(event.c.id, ondelete='CASCADE')),
    Column('invited_id', Integer, ForeignKey(user.c.id, ondelete='CASCADE')),
    UniqueConstraint('event_id', 'invited_id', name='_event_invited_uc'),)
