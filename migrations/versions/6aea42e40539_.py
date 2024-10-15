"""empty message

Revision ID: 6aea42e40539
Revises: 
Create Date: 2024-10-14 21:04:24.922799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6aea42e40539'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Title', sa.String(length=500), nullable=False),
    sa.Column('Author', sa.String(length=100), nullable=False),
    sa.Column('Email', sa.String(length=500), nullable=False),
    sa.Column('Slug', sa.String(length=200), nullable=False),
    sa.Column('blog_post', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Username', sa.String(length=500), nullable=False),
    sa.Column('Name', sa.String(length=100), nullable=False),
    sa.Column('Email', sa.String(length=100), nullable=False),
    sa.Column('Password', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('post')
    # ### end Alembic commands ###