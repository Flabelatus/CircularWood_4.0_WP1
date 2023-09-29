"""08-02-'23

Revision ID: 244bd2d50413
Revises: 
Create Date: 2023-08-02 17:50:43.878624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '244bd2d50413'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('residual_wood', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('residual_wood', schema=None) as batch_op:
        batch_op.drop_column('image')
        batch_op.drop_column('name')

    # ### end Alembic commands ###