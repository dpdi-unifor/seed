"""add_new_attributes

Revision ID: bd363a0d9bb4
Revises: be218984140b
Create Date: 2019-04-05 08:44:25.475785

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import LONGTEXT


# revision identifiers, used by Alembic.
revision = 'bd363a0d9bb4'
down_revision = 'be218984140b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deployment_target', sa.Column('descriptor', LONGTEXT, nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('deployment_target', 'descriptor')
    # ### end Alembic commands ###
