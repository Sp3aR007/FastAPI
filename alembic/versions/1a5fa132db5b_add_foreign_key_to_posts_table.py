"""add foreign key to posts table

Revision ID: 1a5fa132db5b
Revises: 6d150dead9df
Create Date: 2023-03-26 23:55:46.425664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a5fa132db5b'
down_revision = '6d150dead9df'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', "posts", "users",[ "owner_id"], ["id"], ondelete="CASCADE" )
    pass


def downgrade() :
    op.drop_constraint("posts_users_fk","posts")
    op.drop_column("posts", "owner_id")
    pass
