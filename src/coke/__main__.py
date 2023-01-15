from coke.models import Foo
from coke.db import Session


def main():
    """
    For demonstration purposes.

    These checks are also replicated in Pytest.
    """
    session = Session()

    foo1 = Foo(label='one')
    foo2 = Foo(label='two')
    foo3 = Foo(label='three')

    session.add_all([foo1, foo2, foo3])
    session.commit()
    print("insert - ok")

    session.query(Foo).filter(Foo.label == foo1.label).one()
    print("retrieve - ok")

    foo2_new_label = 'twotwo'
    foo2.label = foo2_new_label
    session.commit()
    session.query(Foo).filter(Foo.label == foo2.label).one()
    print("update - ok")

    session.delete(foo3)
    session.commit()
    if session.query(Foo).filter(Foo.label == foo3.label).one_or_none() is None:
        print("delete - ok")


if __name__ == "__main__":
    main()
