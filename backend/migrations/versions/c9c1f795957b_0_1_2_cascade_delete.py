"""0.1.2 Cascade delete

Revision ID: c9c1f795957b
Revises: 18e77acb34af
Create Date: 2022-04-25 14:59:57.971497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9c1f795957b'
down_revision = '18e77acb34af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('dailytask_ibfk_1', 'dailytask', type_='foreignkey')
    op.create_foreign_key(None, 'dailytask', 'user', ['user'], ['uid'], ondelete='CASCADE')
    op.create_foreign_key(None, 'daystate', 'user', ['user'], ['uid'], ondelete='CASCADE')
    op.drop_constraint('jsondoc_ibfk_1', 'jsondoc', type_='foreignkey')
    op.create_foreign_key(None, 'jsondoc', 'user', ['user'], ['uid'], ondelete='CASCADE')
    op.drop_constraint('markdown_ibfk_1', 'markdown', type_='foreignkey')
    op.create_foreign_key(None, 'markdown', 'user', ['user'], ['uid'], ondelete='CASCADE')
    op.drop_constraint('regulartask_ibfk_1', 'regulartask', type_='foreignkey')
    op.create_foreign_key(None, 'regulartask', 'user', ['user'], ['uid'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'regulartask', type_='foreignkey')
    op.create_foreign_key('regulartask_ibfk_1', 'regulartask', 'user', ['user'], ['uid'])
    op.drop_constraint(None, 'markdown', type_='foreignkey')
    op.create_foreign_key('markdown_ibfk_1', 'markdown', 'user', ['user'], ['uid'])
    op.drop_constraint(None, 'jsondoc', type_='foreignkey')
    op.create_foreign_key('jsondoc_ibfk_1', 'jsondoc', 'user', ['user'], ['uid'])
    op.drop_constraint(None, 'daystate', type_='foreignkey')
    op.drop_constraint(None, 'dailytask', type_='foreignkey')
    op.create_foreign_key('dailytask_ibfk_1', 'dailytask', 'user', ['user'], ['uid'])
    # ### end Alembic commands ###
