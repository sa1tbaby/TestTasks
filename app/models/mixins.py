import logging
from sqlalchemy import Column, INTEGER

logger = logging.getLogger(__name__)

class CreateUpdateMixin:
    id = Column(
        INTEGER,
        primary_key=True,
        unique=True,
        autoincrement=True
    )

    created_by = Column(
        INTEGER
    )

