import importlib
import logging

from app.database.metadata import DeclarativeBase

from pydantic import BaseModel as PydanticBaseModel, Extra


class BaseModel(PydanticBaseModel):

    class Config:
        orm_mode = True
        extra = Extra.allow

