"""delete employees column

Revision ID: db064da1324b
Revises: c71bf9b6d292
Create Date: 2024-06-07 11:34:07.896155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db064da1324b'
down_revision: Union[str, None] = 'c71bf9b6d292'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('departments', 'employees')

def downgrade():
    op.add_column('departments', sa.Column('employees', sa.Integer()))
