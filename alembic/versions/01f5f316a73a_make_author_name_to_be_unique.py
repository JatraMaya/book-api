"""Make Author.name to be unique

Revision ID: 01f5f316a73a
Revises: 31bde98399b1
Create Date: 2025-12-11 11:14:20.381297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '01f5f316a73a'
down_revision: Union[str, Sequence[str], None] = '31bde98399b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
