"""Categories unique (event_id, name)

Revision ID: f2f134dce486
Revises: 85f5118d7d9d
Create Date: 2019-10-08 10:34:24.739071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2f134dce486'
down_revision = '85f5118d7d9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_event_name_uc', 'Categories', ['event_id', 'name'])
    op.drop_index('ix_Categories_name', table_name='Categories')
    op.create_index(op.f('ix_Categories_name'), 'Categories', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Categories_name'), table_name='Categories')
    op.create_index('ix_Categories_name', 'Categories', ['name'], unique=True)
    op.drop_constraint('_event_name_uc', 'Categories', type_='unique')
    # ### end Alembic commands ###
