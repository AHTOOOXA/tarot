"""app_language_code

Revision ID: 9620fa1bcc91
Revises: 8dd5c57c17a2
Create Date: 2024-11-17 09:38:46.292666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9620fa1bcc91'
down_revision: Union[str, None] = '8dd5c57c17a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add column as nullable first
    op.add_column('users', sa.Column('app_language_code', sa.String(), nullable=True))

    # 2. Set default value for existing records
    op.execute("UPDATE users SET app_language_code = 'en' WHERE app_language_code IS NULL")

    # 3. Make the column non-nullable
    op.alter_column('users', 'app_language_code',
                    existing_type=sa.String(),
                    nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'app_language_code')
