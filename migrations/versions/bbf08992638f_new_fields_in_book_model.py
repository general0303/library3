"""new fields in book  model

Revision ID: bbf08992638f
Revises: 7989ed950fca
Create Date: 2020-10-29 18:28:44.621445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbf08992638f'
down_revision = '7989ed950fca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('text', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'text')
    # ### end Alembic commands ###
