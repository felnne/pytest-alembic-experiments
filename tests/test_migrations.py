# noinspection PyUnresolvedReferences
import pytest

from pytest_alembic.tests import test_single_head_revision as single_head_revision
from pytest_alembic.tests import test_upgrade as upgrade
from pytest_alembic.tests import test_up_down_consistency as up_down_consistency

# from pytest_alembic.tests import test_model_definitions_match_ddl


class TestMigrations:
    def test_single_head_revision(self, ephemeral_alembic_runner):
        single_head_revision(ephemeral_alembic_runner)

    def test_upgrade(self, ephemeral_alembic_runner):
        upgrade(ephemeral_alembic_runner)

    def test_up_down_consistency(self, ephemeral_alembic_runner):
        up_down_consistency(ephemeral_alembic_runner)
