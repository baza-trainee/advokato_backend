"""empty message

Revision ID: 3665feecc980
Revises: 505d869abe48
Create Date: 2023-12-01 11:59:10.216033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3665feecc980"
down_revision = "505d869abe48"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("specializations", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("specialization_photo", sa.String(length=300), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "specialization_description", sa.String(length=1000), nullable=True
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("specializations", schema=None) as batch_op:
        batch_op.drop_column("specialization_description")
        batch_op.drop_column("specialization_photo")

    # ### end Alembic commands ###