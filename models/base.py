from sqlalchemy import Column, BigInteger, DateTime, text, func

from database import Base, db_session


class BaseTable(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, index=True, server_default=text("id_generator()"))
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def save(self, flush=True, session=None):
        if session is None:
            session = db_session

        session.add(self)
        if flush:
            session.flush()

        return self
