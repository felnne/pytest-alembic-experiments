# noinspection PyUnresolvedReferences
import pytest

from pytest_alembic.tests import test_single_head_revision as single_head_revision
from pytest_alembic.tests import test_upgrade as upgrade
from pytest_alembic.tests import test_up_down_consistency as up_down_consistency
from pytest_alembic.tests import test_model_definitions_match_ddl as model_definitions_match_ddl


class TestMigrations:
    def test_single_head_revision(self, fx_alembic_runner_ephmrl):
        single_head_revision(fx_alembic_runner_ephmrl)

    def test_upgrade(self, fx_alembic_runner_ephmrl):
        upgrade(fx_alembic_runner_ephmrl)

    def test_up_down_consistency(self, fx_alembic_runner_ephmrl):
        up_down_consistency(fx_alembic_runner_ephmrl)

    def test_model_definitions_match_ddl(self, fx_alembic_runner_ephmrl):
        model_definitions_match_ddl(fx_alembic_runner_ephmrl)
