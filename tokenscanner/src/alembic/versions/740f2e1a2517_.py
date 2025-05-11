"""empty message

Revision ID: 740f2e1a2517
Revises: 3c8ced925918
Create Date: 2025-05-11 22:44:53.507466

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "740f2e1a2517"
down_revision: Union[str, None] = "3c8ced925918"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
