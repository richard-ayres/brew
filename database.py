import uuid

import sqlalchemy.types as types

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////var/www/brew/brew.sqlite3', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def uuidgen():
    """Return a UUID, often for database primary keys"""
    return uuid.uuid4()
    # return str(uuid.uuid4())


class UUID(types.UserDefinedType):
    """UUID SQLAlchemy database type"""

    length = 36

    def get_col_spec(self):
        return "CHAR(%d)" % self.length

    def bind_processor(self, dialect):
        def process(value):
            if isinstance(value, uuid.UUID):
                value = str(value)
            if value is None:
                return None
            return value.lower()
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            assert isinstance(value, str)
            return uuid.UUID(value)
        return process

