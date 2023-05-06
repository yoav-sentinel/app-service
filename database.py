from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DATABASE_URL


def create_scoped_session(engine=None):
    if engine is None:
        engine = create_engine()

    return scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    )


db_engine = create_engine(DATABASE_URL)
db_session = create_scoped_session(db_engine)

Base = declarative_base()
