from sqlalchemy import Column, INTEGER, VARCHAR

from app.database.metadata import DeclarativeBase
from app.models.mixins import CreateUpdateMixin


class Image(DeclarativeBase, CreateUpdateMixin):
    """
    """
    __tablename__ = "image"

    path = Column(
        VARCHAR
    )

    name_hash = Column(
        VARCHAR
    )

    type = Column(
        VARCHAR
    )
