"""add last few columns to the table

Revision ID: f740e981e3cc
Revises: 1a5fa132db5b
Create Date: 2023-03-27 00:02:09.124640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f740e981e3cc'
down_revision = '1a5fa132db5b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        "published", sa.Boolean(), nullable=False, server_default='True',
    ))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')
    ))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
