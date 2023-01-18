from datetime import datetime

# noinspection PyUnresolvedReferences
import pytest
from ulid import parse as parse_ulid

from coke.models import Asset


class TestFoo:
    _fid = parse_ulid('01GQ02ZSXFX2SEC05PPQR0HFVD')
    _label = 'foo1'
    _platform_type = 'ship'
    _identifiers = [{"foo": "bar"}]

    def test_asset_object(self):
        asset1 = Asset(
            fid=str(self._fid),
            label=self._label,
            platform_type=self._platform_type,
            identifiers=self._identifiers
        )

        assert asset1.fid == self._fid
        assert asset1.label == self._label
        assert asset1.platform_type == self._platform_type
        assert asset1.identifiers == self._identifiers

    def test_asset_insert(self, fx_db_session):
        asset1 = Asset(
            fid=str(self._fid),
            label=self._label,
            platform_type=self._platform_type,
            identifiers=self._identifiers
        )
        fx_db_session.add(asset1)
        fx_db_session.commit()
        fx_db_session.refresh(asset1)

        assert asset1.id == 1
        assert asset1.identifiers == self._identifiers
        assert isinstance(asset1.inserted_at, datetime)
        assert isinstance(asset1.updated_at, datetime)
        assert asset1.inserted_at == asset1.updated_at

    def test_asset_retrieve(self, fx_db_session):
        asset1 = Asset(fid=str(self._fid), label=self._label, platform_type=self._platform_type)
        fx_db_session.add(asset1)
        fx_db_session.commit()

        fx_db_session.query(Asset).filter(Asset.fid == asset1.fid).one()

    def test_asset_update(self, fx_db_session):
        asset1 = Asset(fid=str(self._fid), label=self._label, platform_type=self._platform_type)
        fx_db_session.add(asset1)
        fx_db_session.commit()

        _new_label = 'asset1'
        asset1.label = _new_label
        fx_db_session.commit()

        fx_db_session.query(Asset).filter(Asset.label == _new_label).one()
        assert isinstance(asset1.inserted_at, datetime)
        assert isinstance(asset1.updated_at, datetime)
        assert asset1.inserted_at == asset1.updated_at

    def test_asset_delete(self, fx_db_session):
        asset1 = Asset(fid=str(self._fid), label=self._label, platform_type=self._platform_type)
        fx_db_session.add(asset1)
        fx_db_session.commit()

        fx_db_session.delete(asset1)
        fx_db_session.commit()

        assert fx_db_session.query(Asset).filter(Asset.fid == asset1.fid).one_or_none() is None
