"""added posts table

Revision ID: 0d5932494973
Revises: 
Create Date: 2023-03-26 22:30:08.838224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d5932494973'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key= True),
    sa.Column('title', sa.String(), nullable=False))
    pass

def downgrade():
    op.drop_table('posts')
    pass
