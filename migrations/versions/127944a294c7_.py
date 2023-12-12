"""empty message

Revision ID: 127944a294c7
Revises: f5ed6053354c
Create Date: 2023-12-12 13:43:17.568709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '127944a294c7'
down_revision = 'f5ed6053354c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pro_bono', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.String(length=3000),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pro_bono', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=3000),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=False)

    # ### end Alembic commands ###