"""added column to the posts table

Revision ID: b948d029cf3f
Revises: 0d5932494973
Create Date: 2023-03-26 23:00:31.976034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b948d029cf3f'
down_revision = '0d5932494973'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column("posts", sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
