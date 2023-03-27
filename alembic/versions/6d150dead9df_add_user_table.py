"""add user table

Revision ID: 6d150dead9df
Revises: b948d029cf3f
Create Date: 2023-03-26 23:06:08.904503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d150dead9df'
down_revision = 'b948d029cf3f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
