"""empty message

Revision ID: 659c16958ff7
Revises: 127944a294c7
Create Date: 2023-12-12 18:33:01.061623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '659c16958ff7'
down_revision = '127944a294c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('about_company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('photo_path', sa.String(length=300), nullable=False),
    sa.Column('description', sa.String(length=3000), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('possibilities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('short_text', sa.String(length=300), nullable=False),
    sa.Column('photo_path', sa.String(length=300), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    with op.batch_alter_table('specializations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('specialization_description_full', sa.String(length=3000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('specializations', schema=None) as batch_op:
        batch_op.drop_column('specialization_description_full')

    op.drop_table('possibilities')
    op.drop_table('about_company')
    # ### end Alembic commands ###
