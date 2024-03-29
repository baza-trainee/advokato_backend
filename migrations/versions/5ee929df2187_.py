"""empty message

Revision ID: 5ee929df2187
Revises: f6a43cef06e6
Create Date: 2023-12-17 23:20:18.670352

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5ee929df2187"
down_revision = "f6a43cef06e6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("cities", schema=None) as batch_op:
        batch_op.add_column(sa.Column("latitude", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("longitude", sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("cities", schema=None) as batch_op:
        batch_op.drop_column("longitude")
        batch_op.drop_column("latitude")

    # ### end Alembic commands ###
