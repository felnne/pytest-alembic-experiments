import pytest
import sqlalchemy


@pytest.fixture
def alembic_engine():
    """Override this fixture to provide pytest-alembic powered tests with a database handle.
    """
    return sqlalchemy.create_engine("postgresql://felnne@localhost/pytest_alembic")


@pytest.fixture
def ephemeral_alembic_runner(alembic_runner):
    yield alembic_runner
    alembic_runner.migrate_down_to('base')
