"""empty message

Revision ID: 686d4f6633fa
Revises: 
Create Date: 2017-03-22 11:01:46.159006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '686d4f6633fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=45), nullable=True),
    sa.Column('last_name', sa.String(length=45), nullable=True),
    sa.Column('address', sa.String(length=45), nullable=True),
    sa.Column('zip', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=45), nullable=True),
    sa.Column('email', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=45), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('imgurl', sa.String(length=120), nullable=True),
    sa.Column('price', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=45), nullable=False),
    sa.Column('password', sa.String(length=45), nullable=False),
    sa.Column('username', sa.String(length=45), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('challenge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=300), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_has_user',
    sa.Column('user_id1', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('user_id2', sa.Integer(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id1'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id2'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id1', 'user_id2')
    )
    op.create_index(op.f('ix_user_has_user_user_id1'), 'user_has_user', ['user_id1'], unique=False)
    op.create_index(op.f('ix_user_has_user_user_id2'), 'user_has_user', ['user_id2'], unique=False)
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('challenge_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['challenge_id'], ['challenge.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    op.drop_index(op.f('ix_user_has_user_user_id2'), table_name='user_has_user')
    op.drop_index(op.f('ix_user_has_user_user_id1'), table_name='user_has_user')
    op.drop_table('user_has_user')
    op.drop_table('challenge')
    op.drop_table('user')
    op.drop_table('product')
    op.drop_table('address')
    # ### end Alembic commands ###
