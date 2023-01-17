"""Add Asset

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

table_name = "asset"


class UtcNow(sa.sql.expression.FunctionElement):
    type = sa.types.DateTime()  # noqa: A003 - third party code so can't use alternate, non-shadowing, name
    inherit_cache = True


@compiles(UtcNow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True, comment="ID"),
        sa.Column("fid", sa.Text(), nullable=False, comment="Feature ID"),
        sa.Column("label", sa.Text(), nullable=False, comment="Label"),
        sa.Column("platform_type", sa.Text(), nullable=False, comment="Platform type"),
        # sa.Column("identifiers", pg.JSONB(), comment="Identifiers"),
        sa.Column("identifiers", pg.JSONB(astext_type=None), comment="Identifiers")

        # sa.Column(
        #     "inserted_at", pg.TIMESTAMP(timezone=True), server_default=UtcNow(), nullable=False, comment="Created at"
        # ),
        # sa.Column(
        #     "updated_at",
        #     pg.TIMESTAMP(timezone=True),
        #     server_default=UtcNow(),
        #     nullable=False,
        #     comment="Last modified at",
        # ),
    )
    op.create_table_comment(table_name=table_name, comment="All assets")
    op.create_unique_constraint(constraint_name=f"uq_{table_name}_fid", table_name=table_name, columns=["fid"])


def downgrade() -> None:
    op.drop_constraint(constraint_name=f"uq_{table_name}_fid", table_name=table_name)
    op.drop_table_comment(table_name=table_name)
    op.drop_table(table_name=table_name)
