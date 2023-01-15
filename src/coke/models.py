from sqlalchemy import Column, Integer, Text, Identity, VARCHAR, PrimaryKeyConstraint, CheckConstraint

from coke.db import Base


class Foo(Base):
    __tablename__ = 'foo'
    __table_args__ = {
        'comment': 'Foo'
    }

    id = Column("id", Integer, Identity(), primary_key=True, comment="ID")
    label = Column("label", Text, nullable=False, comment='Label')

    def __repr__(self):
        return f"<Foo [{self.id}] '{self.label}'>"


class PostGISSpatialRefSys(Base):
    """
    Utility table generated by the PostGIS extension.

    Needed for the DDL migration test to pass. It is never used from within code and can be safely ignored.
    """
    __tablename__ = 'spatial_ref_sys'
    __table_args__ = (
        PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey'),
        CheckConstraint('(srid > 0) AND (srid <= 998999)', name='spatial_ref_sys_srid_check'),
    )

    srid = Column('srid', Integer, autoincrement=False, nullable=False)
    auth_name = Column('auth_name', VARCHAR(length=256), autoincrement=False, nullable=True)
    auth_srid = Column('auth_srid', Integer, autoincrement=False, nullable=True)
    srtext = Column('srtext', VARCHAR(length=2048), autoincrement=False, nullable=True)
    proj4text = Column('proj4text', VARCHAR(length=2048), autoincrement=False, nullable=True)
