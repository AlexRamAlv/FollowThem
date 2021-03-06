"""first migration

Revision ID: a226b489fb9a
Revises: 
Create Date: 2022-06-19 18:55:10.408876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a226b489fb9a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('administrators',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('providers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['administrators.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['administrators.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requesters',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('work_as', sa.String(length=100), nullable=False),
    sa.Column('department', sa.String(length=100), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['administrators.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['administrators.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('requester_id', sa.Integer(), nullable=False),
    sa.Column('request_number', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('comments', sa.Text(), nullable=False),
    sa.Column('requested_at', sa.DateTime(), nullable=True),
    sa.Column('received', sa.String(length=25), nullable=False),
    sa.Column('purchase_order_number', sa.String(length=50), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['administrators.id'], ),
    sa.ForeignKeyConstraint(['requester_id'], ['requesters.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['updated_by_id'], ['administrators.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('request_providers',
    sa.Column('request_id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], ),
    sa.ForeignKeyConstraint(['request_id'], ['requests.id'], ),
    sa.PrimaryKeyConstraint('request_id', 'provider_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request_providers')
    op.drop_table('requests')
    op.drop_table('requesters')
    op.drop_table('providers')
    op.drop_table('administrators')
    # ### end Alembic commands ###
