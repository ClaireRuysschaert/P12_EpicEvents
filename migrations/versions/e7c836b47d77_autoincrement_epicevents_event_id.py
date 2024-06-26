"""autoincrement epicevents event id

Revision ID: e7c836b47d77
Revises: 674f92159d0a
Create Date: 2024-06-21 14:16:05.603051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7c836b47d77'
down_revision: Union[str, None] = '674f92159d0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('epic_event', 'event_id', existing_type=sa.Integer(), autoincrement=True, existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('epic_event', 'event_id', existing_type=sa.Integer(), autoincrement=False, existing_nullable=False)
    # ### end Alembic commands ###
