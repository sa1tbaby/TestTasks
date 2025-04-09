import os

from pydantic import BaseModel as PydanticBaseModel

from app.app_utils.jwt import JWT
from app.dao.image_dao import ImageDao
from app.settings import settings


class FileBody(PydanticBaseModel):
    id: int = 1
    name: str = "test_file"
    fullname: str = "test_file.png"
    type: str = "png"
    created_by: int = 2

    @property
    def content(self) -> bytes:
        with open(f"{self.name}.{self.type}", "rb") as file:
            return file.read()

    @property
    def name_hash(self) -> str:
        name_hash = ImageDao.file_hash(self.name)
        return name_hash[2:]

    @property
    def path(self):
        name_hash = ImageDao.file_hash(self.name)
        return os.path.join(settings.STORE_PATH, name_hash[:2], f"{self.name_hash}.{self.type}")

    def dict(self, *args, **kwargs):
        """Override dict method to include property."""
        d = super().dict(*args, **kwargs)
        d['path'] = self.path
        d['content'] = self.content
        d['name_hash'] = self.name_hash
        return d

class AuthBody(PydanticBaseModel):
    id: int = 2
    created_by: int = 1
    name: str = "admin_2"
    password: str = "admin_2"
    hashed_password: str = JWT.get_password_hash("admin_2")