"""migration_0_1

Revision ID: 8bc7f101397d
Revises: 
Create Date: 2025-12-17 20:42:03.083145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bc7f101397d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table('chat_users', 'chat_members')
    with op.batch_alter_table('chat_members', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_ignored', sa.Boolean(), server_default=sa.text('0'), nullable=False))
        batch_op.add_column(sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('0'), nullable=False))
        batch_op.alter_column('full_name', existing_type=sa.String(), nullable=True)
    op.execute("""
               UPDATE chat_members
               SET is_ignored = 1
               WHERE EXISTS (
                   SELECT 1 FROM exceptions
                   WHERE exceptions.chat_id = chat_members.chat_id
                     AND (
                       exceptions.identifier = CAST(chat_members.user_id AS VARCHAR)
                           OR exceptions.identifier = '@' || chat_members.username
                       )
               )
               """)
    op.drop_table('exceptions')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table('exceptions',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('identifier', sa.VARCHAR(), nullable=False),
                    sa.Column('chat_id', sa.BIGINT(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.execute("""
               INSERT INTO exceptions (identifier, chat_id)
               SELECT CAST(user_id AS VARCHAR), chat_id
               FROM chat_members
               WHERE is_ignored = 1
               """)
    with op.batch_alter_table('chat_members', schema=None) as batch_op:
        batch_op.execute("UPDATE chat_members SET full_name = 'Unknown' WHERE full_name IS NULL")
        batch_op.alter_column('full_name', existing_type=sa.String(), nullable=False)
        batch_op.drop_column('is_deleted')
        batch_op.drop_column('is_ignored')
    op.rename_table('chat_members', 'chat_users')
