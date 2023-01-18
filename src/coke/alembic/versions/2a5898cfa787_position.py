"""Add AssetPosition

Revision ID: 2a5898cfa787
Revises: 21daeed6a2a5
Create Date: 2022-12-16 19:22:36.737824

"""
from enum import Enum

import geoalchemy2.types as ga
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from alembic import op
from sqlalchemy.ext.compiler import compiles

# revision identifiers, used by Alembic.
revision = "2a5898cfa787"
down_revision = "21daeed6a2a5"
branch_labels = None
depends_on = None

table_name = "position"


class GeometryDimensions(Enum):
    _2D = "2D"
    _3D = "3D"


geom_dimensions = pg.ENUM(GeometryDimensions, name="geom_dimensions")


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
        sa.Column(
            "asset_id",
            sa.Integer,
            sa.ForeignKey("asset.id", name="fk_position_asset_id"),
            nullable=False,
            comment="Asset Foreign Key",
        ),
        sa.Column("fid", sa.Text(), nullable=False, comment="Feature ID"),
        sa.Column("datetime", pg.TIMESTAMP(timezone=True), nullable=False, comment="Position observed at"),
        sa.Column(
            "geom",
            ga.Geometry(geometry_type="POINTZ", srid=4326, spatial_index=True, dimension=3),
            nullable=False,
            comment="3D point geometry",
        ),
        sa.Column(
            "geom_dimensions", geom_dimensions, nullable=False, comment="Significant `geom` dimensions (2 = 2D, 3 = 3D)"
        ),
        sa.Column("heading", sa.REAL(), comment="Heading (degrees)"),
        sa.Column("velocity", sa.REAL(), comment="Velocity (m/s)"),
        sa.Column(
            "inserted_at", pg.TIMESTAMP(timezone=True), server_default=UtcNow(), nullable=False, comment="Row created at"
        )
    )
    op.create_table_comment(table_name=table_name, comment="All asset observations/positions")
    op.create_unique_constraint(constraint_name=f"uq_{table_name}_fid", table_name=table_name, columns=["fid"])


def downgrade() -> None:
    op.drop_constraint(constraint_name=f"uq_{table_name}_fid", table_name=table_name)
    op.drop_table_comment(table_name=table_name)
    op.drop_table(table_name=table_name)
    geom_dimensions.drop(op.get_bind())
