from enum import Enum

from sqlalchemy import Column, Integer, String, UniqueConstraint

from database import db_session
from models.base import BaseTable


class AppStatus(Enum):

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
        return [st.value for st in AppStatus]


class Application(BaseTable):
    __tablename__ = "applications"
    #  TODO: change app_status to be ENUM
    developer_id = Column(Integer, nullable=False)
    app_name = Column(String, nullable=False)
    app_status = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('developer_id', 'app_name', name='_developer_id_app_name_uc'),
    )

    #  TODO: consider moving to another file
    FILTERS_TO_COLUMNS = {
        "developer_id": developer_id,
        "app_name": app_name,
        "app_status": app_status
    }

    @classmethod
    def get_by_id(cls, app_id, session=None):
        if not session:
            session = db_session
        print(db_session)
        return session.query(cls).filter(cls.id == app_id).one_or_none()

    @classmethod
    def get_dummy_object(cls, **kwargs):
        app = Application(developer_id=kwargs.get('developer_id', '123'),
                          app_name=kwargs.get('app_name', 'app_name'),
                          app_status=kwargs.get('app_status', AppStatus.NOT_UPLOADED.value))
        return app
