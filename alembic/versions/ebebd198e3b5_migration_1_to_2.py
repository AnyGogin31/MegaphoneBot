"""migration_1_to_2

Revision ID: ebebd198e3b5
Revises: 8bc7f101397d
Create Date: 2026-01-14 22:35:31.137054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebebd198e3b5'
down_revision: Union[str, Sequence[str], None] = '8bc7f101397d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('ignored_users',
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.Column('chat_id', sa.BigInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('user_id', 'chat_id', name=op.f('pk_ignored_users')),
                    )

    op.execute("""
               INSERT INTO ignored_users (user_id, chat_id)
               SELECT user_id, chat_id
               FROM chat_members
               WHERE is_ignored = true
                 AND is_deleted = false
                   ON CONFLICT DO NOTHING;
               """)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('ignored_users')
