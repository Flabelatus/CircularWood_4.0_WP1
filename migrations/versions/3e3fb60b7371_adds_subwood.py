"""adds subwood

Revision ID: 3e3fb60b7371
Revises: ab5c86f57e2d
Create Date: 2024-03-15 18:12:05.663814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e3fb60b7371'
down_revision = 'ab5c86f57e2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sub_wood',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('length', sa.Float(precision=2), nullable=True),
    sa.Column('width', sa.Float(precision=2), nullable=True),
    sa.Column('height', sa.Float(precision=2), nullable=True),
    sa.Column('density', sa.Float(precision=2), nullable=True),
    sa.Column('color', sa.String(length=80), nullable=True),
    sa.Column('timestamp', sa.String(), nullable=True),
    sa.Column('updated_at', sa.String(), nullable=True),
    sa.Column('deleted_at', sa.String(), nullable=True),
    sa.Column('source', sa.String(length=256), nullable=True),
    sa.Column('info', sa.String(length=256), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('project_label', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('wood_id', sa.Integer(), nullable=True),
    sa.Column('design_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['design_id'], ['requirements.id'], name=op.f('fk_sub_wood_design_id_requirements')),
    sa.ForeignKeyConstraint(['wood_id'], ['wood.id'], name=op.f('fk_sub_wood_wood_id_wood')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_sub_wood'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sub_wood')
    # ### end Alembic commands ###
