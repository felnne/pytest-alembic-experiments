from datetime import datetime, timezone

# noinspection PyUnresolvedReferences
import pytest
from ulid import parse as parse_ulid
from geoalchemy2.shape import to_shape, from_shape
from shapely import Point

from coke.models import Asset, AssetPosition, GeometryDimensions


class TestFoo:
    _fid1 = parse_ulid('01GQ02ZSXFX2SEC05PPQR0HFVD')
    _fid2 = parse_ulid('01GQ25Q8R8PGT4GV89DXH87PY2')

    _label = 'foo1'
    _platform_type = 'ship'
    _identifiers = [{"foo": "bar"}]

    _a_id = 1
    _dt = datetime.now(tz=timezone.utc)
    _geom = shape=Point(1, 2, 3)
    _h = 1.0
    _v = 2.0

    def test_asset_object(self):
        asset1 = Asset(
            fid=str(self._fid1),
            label=self._label,
            platform_type=self._platform_type,
            identifiers=self._identifiers
        )

        assert asset1.fid == self._fid1
        assert asset1.label == self._label
        assert asset1.platform_type == self._platform_type
        assert asset1.identifiers == self._identifiers

    def test_asset_insert(self, fx_db_session):
        asset1 = Asset(
            fid=str(self._fid1),
            label=self._label,
            platform_type=self._platform_type,
            identifiers=self._identifiers
        )
        fx_db_session.add(asset1)
        fx_db_session.commit()
        fx_db_session.refresh(asset1)

        # check automatically assigned values
        assert asset1.id == 1
        assert isinstance(asset1.inserted_at, datetime)
        assert isinstance(asset1.updated_at, datetime)
        assert asset1.inserted_at == asset1.updated_at

        # check types preserved
        assert asset1.identifiers == self._identifiers

    def test_asset_retrieve(self, fx_db_session):
        asset1 = Asset(fid=str(self._fid1), label=self._label, platform_type=self._platform_type)
        fx_db_session.add(asset1)
        fx_db_session.commit()

        fx_db_session.query(Asset).filter(Asset.fid == asset1.fid).one()

    def test_asset_update(self, fx_db_session):
        asset1 = Asset(fid=str(self._fid1), label=self._label, platform_type=self._platform_type)
        fx_db_session.add(asset1)
        fx_db_session.commit()

        _new_label = 'asset1'
        asset1.label = _new_label
        fx_db_session.commit()

        fx_db_session.query(Asset).filter(Asset.label == _new_label).one()
        assert isinstance(asset1.inserted_at, datetime)
        assert isinstance(asset1.updated_at, datetime)
        assert asset1.inserted_at < asset1.updated_at

    def test_asset_delete(self, fx_db_session):
        asset1 = Asset(fid=str(self._fid1), label=self._label, platform_type=self._platform_type)
        fx_db_session.add(asset1)
        fx_db_session.commit()

        fx_db_session.delete(asset1)
        fx_db_session.commit()

        assert fx_db_session.query(Asset).filter(Asset.fid == asset1.fid).one_or_none() is None

    def test_asset_position_object(self):
        asset_position1 = AssetPosition(
            asset_id=self._a_id,
            fid=str(self._fid2),
            datetime_=self._dt,
            geom=self._geom,
            heading=self._h,
            velocity=self._v
        )
        # noinspection PyProtectedMember
        asset_position1.geom_dimensions = GeometryDimensions._2D

        assert asset_position1.asset_id == self._a_id
        assert asset_position1.fid == self._fid2
        assert asset_position1.datetime_ == self._dt
        assert asset_position1.geom == self._geom
        assert asset_position1.geom_dimensions == GeometryDimensions._2D
        assert asset_position1.heading == self._h
        assert asset_position1.velocity == self._v

    def test_asset_position_insert_2d(self, fx_db_session_with_asset):
        asset_position1 = AssetPosition(
            asset_id=self._a_id,
            fid=str(self._fid2),
            datetime_=self._dt,
            geom=from_shape(self._geom, srid=4326),
            geom_dimensions=GeometryDimensions._2D,
            heading=self._h,
            velocity=self._v
        )

        fx_db_session_with_asset.add(asset_position1)
        fx_db_session_with_asset.commit()
        fx_db_session_with_asset.refresh(asset_position1)

        # check automatically assigned values
        assert asset_position1.id == 1
        assert isinstance(asset_position1.inserted_at, datetime)

        # check types preserved
        assert asset_position1.datetime_ == self._dt
        assert to_shape(asset_position1.geom) == self._geom
        assert asset_position1.geom_dimensions == GeometryDimensions._2D
        assert asset_position1.heading == self._h
        assert asset_position1.velocity == self._v

    def test_asset_position_insert_3d(self, fx_db_session_with_asset):
        asset_position1 = AssetPosition(
            asset_id=self._a_id,
            fid=str(self._fid2),
            datetime_=self._dt,
            geom=from_shape(self._geom, srid=4326),
            geom_dimensions=GeometryDimensions._3D,
            heading=self._h,
            velocity=self._v
        )

        fx_db_session_with_asset.add(asset_position1)
        fx_db_session_with_asset.commit()
        fx_db_session_with_asset.refresh(asset_position1)

        # check automatically assigned values
        assert asset_position1.id == 1

        # check types preserved
        assert to_shape(asset_position1.geom) == self._geom
        assert asset_position1.geom_dimensions == GeometryDimensions._3D

    def test_asset_position_retrieve(self, fx_db_session_with_asset):
        asset_position1 = AssetPosition(
            asset_id=self._a_id,
            fid=str(self._fid2),
            datetime_=self._dt,
            geom=from_shape(self._geom, srid=4326),
            geom_dimensions=GeometryDimensions._2D,
            heading=self._h,
            velocity=self._v
        )

        fx_db_session_with_asset.add(asset_position1)
        fx_db_session_with_asset.commit()

        fx_db_session_with_asset.query(AssetPosition).filter(AssetPosition.fid == asset_position1.fid).one()

    def test_asset_position_delete(self, fx_db_session_with_asset):
        asset_position1 = AssetPosition(
            asset_id=self._a_id,
            fid=str(self._fid2),
            datetime_=self._dt,
            geom=from_shape(self._geom, srid=4326),
            geom_dimensions=GeometryDimensions._3D,
            heading=self._h,
            velocity=self._v
        )

        fx_db_session_with_asset.add(asset_position1)
        fx_db_session_with_asset.commit()
        fx_db_session_with_asset.refresh(asset_position1)

        fx_db_session_with_asset.delete(asset_position1)
        fx_db_session_with_asset.commit()

        assert fx_db_session_with_asset.query(AssetPosition).filter(AssetPosition.fid == asset_position1.fid).one_or_none() is None

    def test_asset_asset_position_fk(self, fx_db_session):
        asset1 = Asset(
            fid='01GQ02ZSXFX2SEC05PPQR0HFVD',
            label='asset1',
            platform_type='ship'
        )

        asset_position1 = AssetPosition(
            asset_id=self._a_id,
            fid=str(self._fid2),
            datetime_=self._dt,
            geom=from_shape(self._geom, srid=4326),
            geom_dimensions=GeometryDimensions._2D,
            heading=self._h,
            velocity=self._v
        )

        fx_db_session.add(asset1)
        fx_db_session.add(asset_position1)
        fx_db_session.commit()
        fx_db_session.refresh(asset1)
        fx_db_session.refresh(asset_position1)

        # check automatically assigned values
        assert asset_position1.asset == asset1
        assert asset1.positions == [asset_position1]
