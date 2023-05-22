"""updates FKs in requirements

Revision ID: a060ae2d2f7e
Revises: bc60b5aa7cbc
Create Date: 2023-05-17 17:47:36.629977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a060ae2d2f7e'
down_revision = 'bc60b5aa7cbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_tags')
    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_tags_name'), ['name'])

    with op.batch_alter_table('woods_requirements_dashboard', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dashboard_requirement_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fk_woods_requirements_dashboard_requirement_id_requirements_from_dashboard', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_woods_requirements_dashboard_dashboard_requirement_id_requirements_from_dashboard'), 'requirements_from_dashboard', ['dashboard_requirement_id'], ['id'])
        batch_op.drop_column('requirement_id')

    with op.batch_alter_table('woods_requirements_gh', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gh_requirement_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fk_woods_requirements_gh_requirement_id_requirements_from_grasshopper', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_woods_requirements_gh_gh_requirement_id_requirements_from_grasshopper'), 'requirements_from_grasshopper', ['gh_requirement_id'], ['id'])
        batch_op.drop_column('requirement_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('woods_requirements_gh', schema=None) as batch_op:
        batch_op.add_column(sa.Column('requirement_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_woods_requirements_gh_gh_requirement_id_requirements_from_grasshopper'), type_='foreignkey')
        batch_op.create_foreign_key('fk_woods_requirements_gh_requirement_id_requirements_from_grasshopper', 'requirements_from_grasshopper', ['requirement_id'], ['id'])
        batch_op.drop_column('gh_requirement_id')

    with op.batch_alter_table('woods_requirements_dashboard', schema=None) as batch_op:
        batch_op.add_column(sa.Column('requirement_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_woods_requirements_dashboard_dashboard_requirement_id_requirements_from_dashboard'), type_='foreignkey')
        batch_op.create_foreign_key('fk_woods_requirements_dashboard_requirement_id_requirements_from_dashboard', 'requirements_from_dashboard', ['requirement_id'], ['id'])
        batch_op.drop_column('dashboard_requirement_id')

    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_tags_name'), type_='unique')

    op.create_table('_alembic_tmp_tags',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', name='uq_tags_name')
    )
    # ### end Alembic commands ###