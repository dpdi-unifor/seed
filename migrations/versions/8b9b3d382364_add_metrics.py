"""Add metrics

Revision ID: 8b9b3d382364
Revises: 77c18eec4020
Create Date: 2019-02-11 09:34:13.442848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b9b3d382364'
down_revision = '77c18eec4020'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deployment_metric',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('parameters', sa.String(length=1000), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('deployment', sa.Column('command', sa.String(length=5000), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('deployment', 'command')
    op.drop_table('deployment_metric')
    # ### end Alembic commands ###
