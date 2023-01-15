from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Text, Identity
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://felnne@localhost/pytest_alembic')
base = declarative_base()
base.metadata.create_all(engine)


class Foo(base):
    __tablename__ = 'foo'

    id = Column("id", Integer, Identity(), primary_key=True, comment="ID")
    label = Column("label", Text, nullable=False)

    def __repr__(self):
        return f"<Foo [{self.id}] '{self.label}'>"


def main():
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

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
