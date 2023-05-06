from sqlalchemy import Column, DateTime, func, Integer

from database import Base, db_session


class BaseTable(Base):
    """
    BaseTable is an abstract base class that provides common columns and functionality
    for all derived database table classes in the project.
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def save(self, flush=True, session=None):
        """
        Saves the current object to the database, optionally flushing the session.
        :param flush: A boolean indicating whether to flush the session (default: True).
        :param session: The database session (optional).
        :return: The saved object.
        """
        if session is None:
            session = db_session

        session.add(self)
        if flush:
            session.flush()

        return self
