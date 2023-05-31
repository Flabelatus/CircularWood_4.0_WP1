"""created_at not required

Revision ID: bb8a591d559c
Revises: f79ee0143ef0
Create Date: 2023-05-31 15:53:36.428505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb8a591d559c'
down_revision = 'f79ee0143ef0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('requirements', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('requirements', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
