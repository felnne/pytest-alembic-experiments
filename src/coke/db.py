from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://felnne@localhost/pytest_alembic')

Base = declarative_base()

Session = sessionmaker(bind=engine)
