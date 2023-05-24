"""refactored requirements from client

Revision ID: f79ee0143ef0
Revises: 14066cfc7ced
Create Date: 2023-05-24 13:38:02.648456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f79ee0143ef0'
down_revision = '14066cfc7ced'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('waste_wood', schema=None) as batch_op:
        batch_op.drop_column('requirements')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('waste_wood', schema=None) as batch_op:
        batch_op.add_column(sa.Column('requirements', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
