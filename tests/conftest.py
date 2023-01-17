import pytest

from coke.db import Engine as DBEngine, Session as DBSession


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


# scope="module"
@pytest.fixture
def fx_db_session(fx_alembic_runner_ephmrl_head):
    """
    Create SQLAlchemy SQL with migrated database.

    By depending on the `fx_alembic_runner_ephmrl_head` fixture, the DB will be automatically migrated to the latest
    migration before this fixture takes over, and likewise, downgrade the DB after this fixture completes.
    """
    session = DBSession()
    yield session
    session.rollback()
    session.close()
