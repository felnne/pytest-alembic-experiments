"""Add Foo

Revision ID: 21daeed6a2a5
Revises: c86b94ff772b
Create Date: 2022-12-16 18:06:24.042483

"""
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from alembic import op
from sqlalchemy.ext.compiler import compiles


# revision identifiers, used by Alembic.
revision = "21daeed6a2a5"
down_revision = "c86b94ff772b"
branch_labels = None
depends_on = None

table_name = "foo"

def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True, comment="ID"),
        sa.Column("label", sa.Text(), nullable=False, comment="Label"),
    )
    op.create_table_comment(table_name=table_name, comment="Foo")


def downgrade() -> None:
    op.drop_table_comment(table_name=table_name)
    op.drop_table(table_name=table_name)
