"""empty message

Revision ID: cff70f0d70ab
Revises: db064da1324b
Create Date: 2024-06-20 14:35:15.716287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cff70f0d70ab'
down_revision: Union[str, None] = 'db064da1324b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
