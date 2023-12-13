"""empty message

Revision ID: 7c12027b44f8
Revises: 659c16958ff7
Create Date: 2023-12-12 19:36:28.103388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7c12027b44f8"
down_revision = "659c16958ff7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("our_team", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("position", sa.String(length=100), nullable=False)
        )
        batch_op.add_column(
            sa.Column("slider_photo_path", sa.String(length=300), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("our_team", schema=None) as batch_op:
        batch_op.drop_column("slider_photo_path")
        batch_op.drop_column("position")

    # ### end Alembic commands ###