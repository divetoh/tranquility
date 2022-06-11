"""0.1.5 Add MemorizeCard Statistic

Revision ID: cb28b4bb59e6
Revises: 4ceee46ca515
Create Date: 2022-06-10 15:16:49.940288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb28b4bb59e6'
down_revision = '4ceee46ca515'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('memorizecardhistory',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('card', sa.Integer(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=False),
    sa.Column('statedate', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['card'], ['memorizecard.uid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_memorizecardhistory_card'), 'memorizecardhistory', ['card'], unique=False)
    op.create_index(op.f('ix_memorizecardhistory_uid'), 'memorizecardhistory', ['uid'], unique=False)
    op.create_index(op.f('ix_memorizecardhistory_user'), 'memorizecardhistory', ['user'], unique=False)
    op.create_table('memorizecardstate',
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('card', sa.Integer(), nullable=False),
    sa.Column('state', sa.Integer(), nullable=False),
    sa.Column('lastdate', sa.Date(), nullable=True),
    sa.Column('nextdate', sa.Date(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['card'], ['memorizecard.uid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user', 'card')
    )
    op.create_index(op.f('ix_memorizecardstate_card'), 'memorizecardstate', ['card'], unique=False)
    op.create_index(op.f('ix_memorizecardstate_user'), 'memorizecardstate', ['user'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_memorizecardstate_user'), table_name='memorizecardstate')
    op.drop_index(op.f('ix_memorizecardstate_card'), table_name='memorizecardstate')
    op.drop_table('memorizecardstate')
    op.drop_index(op.f('ix_memorizecardhistory_user'), table_name='memorizecardhistory')
    op.drop_index(op.f('ix_memorizecardhistory_uid'), table_name='memorizecardhistory')
    op.drop_index(op.f('ix_memorizecardhistory_card'), table_name='memorizecardhistory')
    op.drop_table('memorizecardhistory')
    # ### end Alembic commands ###
