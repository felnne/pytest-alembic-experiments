from ulid import parse as parse_ulid

from coke.models import Asset
from coke.db import Session

_fid1 = parse_ulid('01GQ02ZSXFX2SEC05PPQR0HFVD')
_fid2 = parse_ulid('01GQ030F275C3C12GDA676QHD5')
_fid3 = parse_ulid('01GQ030Q19P7PN0PH36F1MY0TQ')

asset1 = Asset(fid=str(_fid1), label='one', platform_type='ship')
asset2 = Asset(fid=str(_fid2), label='two', platform_type='aircraft')
asset3 = Asset(fid=str(_fid3), label='three', platform_type='aircraft', identifiers=[{'one', 'two'}])


def main():
    """
    For demonstration purposes.

    These checks are also replicated in Pytest.
    """
    session = Session()

    session.add_all([asset1, asset2, asset3])
    session.commit()
    print("insert - ok")

    session.query(Asset).filter(Asset.fid == asset1.fid).one()
    print("retrieve - ok")

    asset2_new_label = 'twotwo'
    asset2.label = asset2_new_label
    session.commit()
    session.query(Asset).filter(Asset.fid == asset2.label).one()
    print("update - ok")

    session.delete(asset3)
    session.commit()
    if session.query(Asset).filter(Asset.fid == asset3.fid).one_or_none() is None:
        print("delete - ok")


if __name__ == "__main__":
    main()
