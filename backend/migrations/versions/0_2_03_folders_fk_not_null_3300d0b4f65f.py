"""0.2.03 Folders FK not null

Revision ID: 3300d0b4f65f
Revises: ff518f802d6a
Create Date: 2022-09-06 18:40:28.834531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3300d0b4f65f'
down_revision = 'ff518f802d6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('jsondoc', 'folder',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('markdown', 'folder',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('markdown', 'folder',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('jsondoc', 'folder',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
