"""first migration

Revision ID: 8360394286bd
Revises: 
Create Date: 2021-01-10 20:52:03.997017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8360394286bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('foo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('foo')
    # ### end Alembic commands ###
