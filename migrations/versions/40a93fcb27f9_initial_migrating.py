"""initial migrating

Revision ID: 40a93fcb27f9
Revises: 4c16054a9d8f
Create Date: 2017-10-06 15:29:18.105451

"""

# revision identifiers, used by Alembic.
revision = '40a93fcb27f9'
down_revision = '4c16054a9d8f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    # ### end Alembic commands ###
