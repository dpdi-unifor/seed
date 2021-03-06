"""optional

Revision ID: abedd6093698
Revises: 9da91a3b53d8
Create Date: 2019-02-11 22:32:38.960714

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'abedd6093698'
down_revision = '9da91a3b53d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('deployment', 'command',
               existing_type=mysql.VARCHAR(length=5000),
               nullable=True)
    op.alter_column('deployment', 'entry_point',
               existing_type=mysql.VARCHAR(length=800),
               nullable=True)
    op.alter_column('deployment', 'image_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('deployment', 'target_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('deployment', 'target_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('deployment', 'image_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('deployment', 'entry_point',
               existing_type=mysql.VARCHAR(length=800),
               nullable=False)
    op.alter_column('deployment', 'command',
               existing_type=mysql.VARCHAR(length=5000),
               nullable=False)
    # ### end Alembic commands ###
