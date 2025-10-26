%!
from alembic import op
import sqlalchemy as sa

%#
% if autogenerate:
% for rev in config.get_section('alembic').get('versions', []):
% endfor
% endif

"""empty message

Revision ID: ${up_revision}
Revises: ${down_revision | None}
Create Date: ${create_date}

"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    pass

def downgrade():
    pass
