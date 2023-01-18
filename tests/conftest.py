import pytest

from coke.db import Engine as DBEngine, Session as DBSession
from coke.models import Asset


@pytest.fixture
def alembic_engine():
    """
    Pytest-alembic required fixture.

    Needs to return a database handle.
    """
    return DBEngine


@pytest.fixture
def fx_alembic_runner_ephmrl(alembic_runner):
    """
    Ephemeral Alembic runner.

    Ensures all tests start and end at base migration.

    Inherits from the pytest-alembic provided `alembic_runner` fixture.
    """
    alembic_runner.migrate_down_to('base')
    yield alembic_runner
    alembic_runner.migrate_down_to('base')


@pytest.fixture
def fx_alembic_runner_ephmrl_head(fx_alembic_runner_ephmrl):
    """
    Ephemeral Alembic runner, upgraded to the latest migration.

    Ensure all tests start with a migrated database and end at base migration.
    """
    fx_alembic_runner_ephmrl.migrate_up_to('head')
    yield fx_alembic_runner_ephmrl
    fx_alembic_runner_ephmrl.migrate_down_to('base')


@pytest.fixture
def fx_db_session(fx_alembic_runner_ephmrl_head):
    """
    Create SQLAlchemy Session with migrated database.

    By depending on the `fx_alembic_runner_ephmrl_head` fixture, the DB will be automatically migrated to the latest
    migration before this fixture takes over, and likewise, downgrade the DB after this fixture completes.
    """
    session = DBSession()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def fx_db_session_with_asset(fx_db_session):
    """
    Create SQLAlchemy Session with migrated database and existing asset.

    This fixture is intended for use when testing AssetPositions, which rely on an existing Asset being present in the
    DB as part of the mandatory foreign key relationship.

    By depending on the `fx_alembic_runner_ephmrl_head` fixture, the DB will be automatically migrated to the latest
    migration and DB session opened, before this fixture takes over. The session will be closed and DB downgraded after
    this fixture completes.
    """
    asset1 = Asset(
        fid='01GQ02ZSXFX2SEC05PPQR0HFVD',
        label='asset1',
        platform_type='ship'
    )
    fx_db_session.add(asset1)
    fx_db_session.commit()
    fx_db_session.refresh(asset1)
    yield fx_db_session
