"""refactored requirements from client

Revision ID: 14066cfc7ced
Revises: a060ae2d2f7e
Create Date: 2023-05-24 11:48:18.988857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14066cfc7ced'
down_revision = 'a060ae2d2f7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requirements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('part_index', sa.String(), nullable=False),
    sa.Column('length', sa.String(), nullable=False),
    sa.Column('width', sa.String(), nullable=False),
    sa.Column('height', sa.String(), nullable=False),
    sa.Column('tag', sa.String(length=80), nullable=True),
    sa.Column('part', sa.String(length=80), nullable=False),
    sa.Column('created_at', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_requirements'))
    )
    op.create_table('woods_requirements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wood_id', sa.Integer(), nullable=True),
    sa.Column('requirement_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['requirement_id'], ['requirements.id'], name=op.f('fk_woods_requirements_requirement_id_requirements')),
    sa.ForeignKeyConstraint(['wood_id'], ['residual_wood.id'], name=op.f('fk_woods_requirements_wood_id_residual_wood')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_woods_requirements'))
    )
    op.drop_table('requirements_from_dashboard')
    op.drop_table('woods_requirements_gh')
    op.drop_table('woods_requirements_dashboard')
    op.drop_table('requirements_from_grasshopper')
    with op.batch_alter_table('residual_wood', schema=None) as batch_op:
        batch_op.drop_column('requirements')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('residual_wood', schema=None) as batch_op:
        batch_op.add_column(sa.Column('requirements', sa.INTEGER(), nullable=True))

    op.create_table('requirements_from_grasshopper',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('part_index', sa.VARCHAR(), nullable=False),
    sa.Column('length', sa.VARCHAR(), nullable=False),
    sa.Column('width', sa.VARCHAR(), nullable=False),
    sa.Column('height', sa.VARCHAR(), nullable=False),
    sa.Column('tag', sa.VARCHAR(length=80), nullable=True),
    sa.Column('part', sa.VARCHAR(length=80), nullable=False),
    sa.Column('created_at', sa.INTEGER(), nullable=False),
    sa.Column('project_id', sa.VARCHAR(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_requirements_from_grasshopper')
    )
    op.create_table('woods_requirements_dashboard',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('dashboard_requirement_id', sa.INTEGER(), nullable=True),
    sa.Column('wood_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['dashboard_requirement_id'], ['requirements_from_dashboard.id'], name='fk_woods_requirements_dashboard_dashboard_requirement_id_requirements_from_dashboard'),
    sa.ForeignKeyConstraint(['wood_id'], ['residual_wood.id'], name='fk_woods_requirements_dashboard_wood_id_residual_wood'),
    sa.PrimaryKeyConstraint('id', name='pk_woods_requirements_dashboard')
    )
    op.create_table('woods_requirements_gh',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('gh_requirement_id', sa.INTEGER(), nullable=True),
    sa.Column('wood_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['gh_requirement_id'], ['requirements_from_grasshopper.id'], name='fk_woods_requirements_gh_gh_requirement_id_requirements_from_grasshopper'),
    sa.ForeignKeyConstraint(['wood_id'], ['residual_wood.id'], name='fk_woods_requirements_gh_wood_id_residual_wood'),
    sa.PrimaryKeyConstraint('id', name='pk_woods_requirements_gh')
    )
    op.create_table('requirements_from_dashboard',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('part_index', sa.VARCHAR(), nullable=False),
    sa.Column('length', sa.VARCHAR(), nullable=False),
    sa.Column('width', sa.VARCHAR(), nullable=False),
    sa.Column('height', sa.VARCHAR(), nullable=False),
    sa.Column('tag', sa.VARCHAR(length=80), nullable=True),
    sa.Column('part', sa.VARCHAR(length=80), nullable=False),
    sa.Column('created_at', sa.INTEGER(), nullable=False),
    sa.Column('project_id', sa.VARCHAR(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_requirements_from_dashboard')
    )
    op.drop_table('woods_requirements')
    op.drop_table('requirements')
    # ### end Alembic commands ###