"""Update ParentChild Table

Revision ID: bb9b2b6493d9
Revises: 671da503e5ce
Create Date: 2022-09-18 18:21:49.517733

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bb9b2b6493d9'
down_revision = '671da503e5ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parent_child', 'invitation_code',
               existing_type=mysql.VARCHAR(length=8),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parent_child', 'invitation_code',
               existing_type=mysql.VARCHAR(length=8),
               nullable=True)
    # ### end Alembic commands ###
