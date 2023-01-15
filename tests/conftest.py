import pytest
import sqlalchemy

@pytest.fixture
def alembic_engine():
    """Override this fixture to provide pytest-alembic powered tests with a database handle.
    """
    return sqlalchemy.create_engine("postgresql://felnne@localhost/pytest_alembic")
