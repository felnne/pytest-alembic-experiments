"""DB extensions

Revision ID: c86b94ff772b
Revises:
Create Date: 2022-12-16 17:51:15.051886

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c86b94ff772b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass
    op.execute(sa.text("CREATE EXTENSION IF NOT EXISTS postgis;"))


def downgrade() -> None:
    pass
    op.execute(sa.text("DROP EXTENSION IF EXISTS postgis;"))
