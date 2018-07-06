"""empty message

Revision ID: 441e678a71ec
Revises: 1b94554d8b21
Create Date: 2018-07-03 10:36:27.636327

"""

# revision identifiers, used by Alembic.
revision = '441e678a71ec'
down_revision = '1b94554d8b21'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reshwap_items', sa.Column('is_completed', sa.Boolean(), nullable=True))
    op.drop_column('reshwap_items', 'isCompleted')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reshwap_items', sa.Column('isCompleted', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('reshwap_items', 'is_completed')
    # ### end Alembic commands ###