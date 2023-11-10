from pathlib import Path

import databases
import sqlalchemy
from sqlalchemy.orm import (scoped_session, sessionmaker)
from sqlalchemy.orm import declarative_base
from starlette.config import Config


# Configuration from environment variables or '.env' file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
config = Config(PROJECT_ROOT.joinpath('.env'))
DATABASE_URL = config('DATABASE_URL')


# lifespan用に作成
database_for_lifespan = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(DATABASE_URL)

_scoped_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

def get_db_session():
    return _scoped_session()

def new_db_session():
    _scoped_session.remove()
    return _scoped_session()
