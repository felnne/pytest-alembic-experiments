from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from coke.config import db_dsn

Engine = create_engine(db_dsn)
Base = declarative_base()
Session = sessionmaker(bind=Engine)
