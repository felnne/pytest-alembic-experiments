import pytest

from coke.db import engine as app_engine, Session as app_session


@pytest.fixture
def alembic_engine():
    """Override this fixture to provide pytest-alembic powered tests with a database handle.
    """
    return app_engine


@pytest.fixture
def alembic_runner_ephmrl(alembic_runner):
    """
    Ephemeral Alembic runner.

    Ensure all tests start and end at base migration."""
    alembic_runner.migrate_down_to('base')
    yield alembic_runner
    alembic_runner.migrate_down_to('base')


@pytest.fixture
def alembic_runner_ephmrl_head(alembic_runner_ephmrl):
    """
    Ephemeral Alembic runner, upgraded to latest migration.

    Ensure all tests start with a migrated database and end at base migration.
    """
    alembic_runner_ephmrl.migrate_up_to('head')
    yield alembic_runner_ephmrl
    alembic_runner_ephmrl.migrate_down_to('base')


# scope="module"
@pytest.fixture
def db_session(alembic_runner_ephmrl_head):
    """
    Create SQLAlchemy SQL with migrated database
    """
    session = app_session()
    yield session
    session.rollback()
    session.close()
