from sqlalchemy import Column, String

from app.database.metadata import DeclarativeBase
from app.models.mixins import CreateUpdateMixin


class User(DeclarativeBase, CreateUpdateMixin):
    """
    """
    __tablename__ = "user"

    name = Column(String, unique=True, index=True)

    hashed_password = Column(String)
