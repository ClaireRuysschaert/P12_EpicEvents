"""add department field on staff_user

Revision ID: c71bf9b6d292
Revises: 8e46025f2aea
Create Date: 2024-06-07 11:24:24.073805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c71bf9b6d292'
down_revision: Union[str, None] = '8e46025f2aea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add department column to StaffUser table
    op.add_column(
        'staff_user',
        sa.Column('department_id', sa.Integer, sa.ForeignKey('departments.id'))
    )


def downgrade() -> None:
    op.drop_column('staff_user', 'department_id')
