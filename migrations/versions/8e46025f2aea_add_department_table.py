"""Add department table

Revision ID: 8e46025f2aea
Revises: e544f6300fb4
Create Date: 2024-06-07 10:53:02.027305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e46025f2aea'
down_revision: Union[str, None] = 'e544f6300fb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create Department table
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False, unique=True),
        sa.Column('employees', sa.Integer, sa.ForeignKey('staff_user.staff_id'))
    )


def downgrade() -> None:
    pass
