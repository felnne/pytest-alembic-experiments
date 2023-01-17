# noinspection PyUnresolvedReferences
import pytest

from coke.models import Foo


class TestFoo:
    _label = 'foo1'

    def test_foo_object(self):
        foo1 = Foo(label=self._label)

        assert foo1.label == self._label

    def test_foo_insert(self, fx_db_session):
        foo1 = Foo(label=self._label)
        fx_db_session.add(foo1)
        fx_db_session.commit()
        fx_db_session.refresh(foo1)

        assert foo1.id == 1

    def test_foo_retrieve(self, fx_db_session):
        foo1 = Foo(label=self._label)
        fx_db_session.add(foo1)
        fx_db_session.commit()

        fx_db_session.query(Foo).filter(Foo.label == foo1.label).one()

    def test_foo_update(self, fx_db_session):
        foo1 = Foo(label=self._label)
        fx_db_session.add(foo1)
        fx_db_session.commit()

        _new_label = 'foo1one'
        foo1.label = _new_label
        fx_db_session.commit()

        fx_db_session.query(Foo).filter(Foo.label == _new_label).one()

    def test_foo_delete(self, fx_db_session):
        foo1 = Foo(label=self._label)
        fx_db_session.add(foo1)
        fx_db_session.commit()

        fx_db_session.delete(foo1)
        fx_db_session.commit()

        assert fx_db_session.query(Foo).filter(Foo.label == foo1.label).one_or_none() is None
