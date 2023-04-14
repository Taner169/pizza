"""empty message

Revision ID: 6b39e3f0f13f
Revises: 
Create Date: 2023-04-12 15:17:03.263226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b39e3f0f13f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contact', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('employee', sa.Column('email', sa.String(length=120), nullable=False))
    op.create_unique_constraint(None, 'employee', ['email'])
    op.drop_column('employee', 'date_created')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('date_created', sa.DATETIME(), nullable=False))
    op.drop_constraint(None, 'employee', type_='unique')
    op.drop_column('employee', 'email')
    op.alter_column('contact', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###