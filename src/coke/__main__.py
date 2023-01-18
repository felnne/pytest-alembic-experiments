from datetime import datetime, timezone

from ulid import parse as parse_ulid

from coke.models import Asset, AssetPosition, GeometryDimensions
from coke.db import Session

_fid1 = parse_ulid('01GQ02ZSXFX2SEC05PPQR0HFVD')
_fid2 = parse_ulid('01GQ030F275C3C12GDA676QHD5')
_fid3 = parse_ulid('01GQ030Q19P7PN0PH36F1MY0TQ')

_fid4 = parse_ulid('01GQ25Q8R8PGT4GV89DXH87PY2')
_fid5 = parse_ulid('01GQ25RDZ91M9DW8P4FMMNN8P1')
_fid6 = parse_ulid('01GQ25RKW3RB2HK2KNA8F9HYH4')
_fid7 = parse_ulid('01GQ25K3EJKCQBBX7PE2BF3HJX')

_dt = datetime.now(tz=timezone.utc)

asset1 = Asset(fid=str(_fid1), label='one', platform_type='ship')
asset2 = Asset(fid=str(_fid2), label='two', platform_type='aircraft')
asset3 = Asset(fid=str(_fid3), label='three', platform_type='aircraft', identifiers=[{'foo': 'bar'}])


assetPosition1 = AssetPosition(
    asset_id=1,
    fid=str(_fid4),
    datetime_=_dt,
    geom="SRID=4326;POINT(1 2 0)"
)
# noinspection PyProtectedMember
assetPosition1.geom_dimensions = GeometryDimensions._2D

assetPosition2 = AssetPosition(
    asset_id=1,
    fid=str(_fid5),
    datetime_=_dt,
    geom="SRID=4326;POINT(1 2 3)"
)
# noinspection PyProtectedMember
assetPosition2.geom_dimensions = GeometryDimensions._3D

assetPosition3 = AssetPosition(
    asset_id=1,
    fid=str(_fid6),
    datetime_=_dt,
    geom="SRID=4326;POINT(1 2 3)",
    heading=1.0
)
# noinspection PyProtectedMember
assetPosition3.geom_dimensions = GeometryDimensions._3D

assetPosition4 = AssetPosition(
    asset_id=1,
    fid=str(_fid7),
    datetime_=_dt,
    geom="SRID=4326;POINT(1 2 3)",
    heading=1.0,
    velocity=2.0
)
# noinspection PyProtectedMember
assetPosition4.geom_dimensions = GeometryDimensions._3D


def asset(session):
    """
    For demonstration purposes.

    These checks are also replicated in Pytest.
    """

    # session.add_all([asset1, asset2, asset3])
    session.add_all([asset1, asset2, asset3])
    session.commit()
    print("Asset insert - ok")

    session.query(Asset).filter(Asset.fid == asset1.fid).one()
    print("Asset retrieve - ok")

    asset2_new_label = 'twotwo'
    asset2.label = asset2_new_label
    session.commit()
    session.query(Asset).filter(Asset.label == asset2_new_label).one()
    print("Asset update - ok")

    session.delete(asset3)
    session.commit()
    if session.query(Asset).filter(Asset.fid == asset3.fid).one_or_none() is None:
        print("Asset delete - ok")


def asset_position(session):
    """
    For demonstration purposes.

    These checks are also replicated in Pytest.
    """

    session.add_all([assetPosition1, assetPosition2, assetPosition3, assetPosition4])
    session.commit()
    print("AssetPosition insert - ok")

    session.query(AssetPosition).filter(AssetPosition.fid == assetPosition1.fid).one()
    print("AssetPosition retrieve - ok")

    # update not checked as Positions are essentially (but not yet formally immutable)

    session.delete(assetPosition3)
    session.commit()
    if session.query(AssetPosition).filter(AssetPosition.fid == assetPosition3.fid).one_or_none() is None:
        print("AssetPosition delete - ok")

    if assetPosition4.asset == asset1:
        print("AssetPosition relationship - ok")


def main():
    session = Session()

    asset(session=session)
    asset_position(session=session)

    # check foreign key property
    if len(asset1.positions) > 0 and asset1.positions[0] == assetPosition1:
        print('Asset / AssetPosition FK check (forward) - ok')
    if assetPosition1.asset == asset1:
        print('Asset / AssetPosition FK check (backward) - ok')


if __name__ == "__main__":
    main()
