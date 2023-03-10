from enum import Enum

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, Text, REAL, Identity, ForeignKeyConstraint, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, ENUM
from sqlalchemy.orm import relationship

from coke.db import Base


class Asset(Base):
    __tablename__ = 'asset'
    __table_args__ = (
        UniqueConstraint("fid", name=f"uq_{__tablename__}_fid"),
        {'comment': 'All assets'}
    )

    id = Column("id", Integer, Identity(), primary_key=True, comment="ID")
    fid = Column("fid", Text, nullable=False, comment='Feature ID')
    label = Column("label", Text, nullable=False, comment='Label')
    platform_type = Column("platform_type", Text, nullable=False, comment='Platform type')
    identifiers = Column("identifiers", JSONB(astext_type=None), comment="Identifiers")
    inserted_at = Column("inserted_at", TIMESTAMP(timezone=True), nullable=False,
                         server_default=text("timezone('utc'::text, CURRENT_TIMESTAMP)"), comment="Row created at")
    updated_at = Column("updated_at", TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("timezone('utc'::text, CURRENT_TIMESTAMP)"), comment="Row last modified at")

    positions = relationship("AssetPosition", back_populates="asset")

    def __repr__(self):
        return f"<Asset ({self.id}) [{self.fid}] '{self.label}' {self.platform_type}>"


class GeometryDimensions(Enum):
    _2D = "2D"
    _3D = "3D"


geom_dimensions = ENUM(GeometryDimensions, name="geom_dimensions")


class AssetPosition(Base):
    __tablename__ = 'position'
    __table_args__ = (
        UniqueConstraint("fid", name=f"uq_{__tablename__}_fid"),
        ForeignKeyConstraint(("asset_id",), ["asset.id"]),
        {'comment': 'All asset observations/positions'}
    )

    id = Column("id", Integer, Identity(), primary_key=True, comment="ID")
    asset_id = Column("asset_id", Integer, nullable=False, comment="Asset Foreign Key")
    fid = Column("fid", Text, nullable=False, comment='Feature ID')
    datetime_ = Column("datetime", TIMESTAMP(timezone=True), nullable=False, comment='Position observed at')
    geom = Column(
        "geom",
        Geometry(geometry_type="POINTZ", srid=4326, spatial_index=True, dimension=3),
        nullable=False,
        comment="3D point geometry",
    )
    geom_dimensions = Column(
        "geom_dimensions", geom_dimensions, nullable=False, comment="Significant `geom` dimensions (2 = 2D, 3 = 3D)"
    )
    heading = Column("heading", REAL(), comment="Heading (degrees)")
    velocity = Column("velocity", REAL(), comment="Velocity (m/s)")
    inserted_at = Column("inserted_at", TIMESTAMP(timezone=True), nullable=False,
                         server_default=text("timezone('utc'::text, CURRENT_TIMESTAMP)"), comment="Row created at")

    asset = relationship("Asset", back_populates="positions")

    def __repr__(self):
        _h = '-'
        if self.heading is not None:
            _h = self.heading
        _v = '-'
        if self.velocity is not None:
            _v = self.velocity

        return f"<AssetPosition ({self.id}) [{self.fid}] @ {self.datetime_}' ({self.geom}) H {_h} V {_v}>"
