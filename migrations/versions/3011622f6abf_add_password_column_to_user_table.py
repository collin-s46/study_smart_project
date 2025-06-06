"""Add password column to User table

Revision ID: 3011622f6abf
Revises: dc618aadbb3a
Create Date: 2025-04-19 19:55:39.393142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3011622f6abf'
down_revision = 'dc618aadbb3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=200), nullable=False))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.VARCHAR(length=128), nullable=False))
        batch_op.alter_column('email',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.drop_column('password')

    # ### end Alembic commands ###
