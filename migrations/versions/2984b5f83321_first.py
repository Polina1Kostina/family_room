"""first

Revision ID: 2984b5f83321
Revises: 
Create Date: 2023-03-06 12:50:36.182554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2984b5f83321'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('family',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_family_name'), 'family', ['name'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('birth_day', sa.Date(), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('family_id', sa.Integer(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('place', sa.String(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_id'), 'event', ['id'], unique=False)
    op.create_index(op.f('ix_event_title'), 'event', ['title'], unique=False)
    op.create_table('event_invited',
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('invited_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['invited_id'], ['user.id'], ),
    sa.UniqueConstraint('event_id', 'invited_id', name='_event_invited_uc')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_invited')
    op.drop_index(op.f('ix_event_title'), table_name='event')
    op.drop_index(op.f('ix_event_id'), table_name='event')
    op.drop_table('event')
    op.drop_table('user')
    op.drop_index(op.f('ix_family_name'), table_name='family')
    op.drop_table('family')
    # ### end Alembic commands ###