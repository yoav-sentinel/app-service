from enum import Enum

from sqlalchemy import Column, Integer, String, UniqueConstraint

from database import db_session
from models.base import BaseTable


class AppStatus(Enum):
    """
    AppStatus is an enumeration class representing the status of an application.
    """

    def __new__(cls, value: str):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    NOT_UPLOADED = 'not_uploaded'
    UNDER_REVIEW = 'under_review'
    REJECTED = 'rejected'
    APPROVED = 'approved'
    DELETED = 'deleted'

    @classmethod
    def app_status_values(cls):
        return {st.value for st in AppStatus}


class Application(BaseTable):
    """
    Application is a class representing an application stored in the database.
    """
    __tablename__ = "applications"
    developer_id = Column(Integer, nullable=False)
    app_name = Column(String, nullable=False)
    app_status = Column(String, nullable=False)  # Not using Enum as it may surface complications on Enum modifications

    __table_args__ = (
        UniqueConstraint('developer_id', 'app_name', name='_developer_id_app_name_uc'),
    )

    # TODO: consider moving to another file
    FILTERS_TO_COLUMNS = {
        "developer_id": developer_id,
        "app_name": app_name,
        "app_status": app_status
    }

    @classmethod
    def get_by_id(cls, app_id, session=None):
        """
        Retrieves an application by its ID.
        :param app_id: The ID of the application.
        :param session: The database session (optional).
        :return: The Application object or None if not found.
        """
        if not session:
            session = db_session
        return session.query(cls).filter(cls.id == app_id).one_or_none()

    @classmethod
    def get_dummy_object(cls, **kwargs):
        """
        Creates a dummy Application object for testing purposes.
        :param kwargs: The optional keyword arguments for the Application object.
        :return: A dummy Application object.
        """
        app = Application(developer_id=kwargs.get('developer_id', '123'),
                          app_name=kwargs.get('app_name', 'app_name'),
                          app_status=kwargs.get('app_status', AppStatus.NOT_UPLOADED.value))
        return app
