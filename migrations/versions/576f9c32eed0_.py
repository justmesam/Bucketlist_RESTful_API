"""empty message

Revision ID: 576f9c32eed0
Revises: 
Create Date: 2017-07-27 15:04:18.397638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '576f9c32eed0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=300), nullable=True),
    sa.Column('password', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('User')
    # ### end Alembic commands ###
