import logging
import os
import hashlib
from fastapi import UploadFile

from app.dao.base_dao import BaseDao
from app.dto.image_dto import ImageReprDto
from app.models import Image
from app.settings import settings

class ImageDao(BaseDao):

    def __init__(self, session, model):
        BaseDao.__init__(self, session, model)

    @classmethod
    def file_hash(cls, text: str, algorithm: str = "sha256") -> str:
        try:
            hash_object = hashlib.new(algorithm, text.encode('utf-8'))
            hex_digest = hash_object.hexdigest()
            return hex_digest
        except ValueError:
            return f"Invalid hashing algorithm: {algorithm}"


    @classmethod
    def _file_repr(cls, file_body: UploadFile) -> ImageReprDto:
        file_name = file_body.filename
        _hash = cls.file_hash(file_name)
        file_name_hash = _hash[2:]

        try:
            # При передаче изображения всегда должен быть Тип файла и его расширение
            # Отсутствие параметра image указывает на неверный тип файла
            # Соответственно remove вернет в таком случае KeyError
            # Поэтому валидацию на размер также ловим по KeyError
            content_type = set(file_body.content_type.split("/"))
            content_type.remove("image")
            if len(content_type) != 1:
                raise KeyError()

        except KeyError as exc:
            msg = "wrong type of file"
            logging.error(msg, exc_info=exc)
            raise KeyError(msg)

        else:
            file_type = content_type.pop()

        file_path = os.path.join(settings.STORE_PATH, _hash[:2], f"{file_name_hash}.{file_type}")

        return ImageReprDto(
            name=file_name,
            name_hash=file_name_hash,
            type=file_type,
            content=file_body.file.read(),
            path=file_path
        )

    async def upload_image(
            self,
            file_body: UploadFile,
            payload: dict
    ):
        try:
            file_dto: ImageReprDto = self._file_repr(file_body)

            try:
                # Получаем путь к каталогу (исключая имя файла)
                directory = os.path.dirname(file_dto.path)
                if directory:
                    os.makedirs(directory, exist_ok=True)

                with open(file_dto.path, "wb") as stored_file:
                    stored_file.write(file_dto.content)

            except Exception as exc:
                logging.error("an exception was caught while trying to save image on a disk")
                raise exc

            else:
                await self.create_one(body={
                    "path": file_dto.path,
                    "name_hash": file_dto.name_hash,
                    "type": file_dto.type,
                    "created_by": payload.get("user_id")
                })

        except Exception as exc:
            logging.error("an exception was caught while trying to upload image", exc_info=exc)
            raise exc

        else:
            return file_dto.name_hash

    async def download_image(
            self,
            **kwargs
    ):
        file_metadata: Image = await self.find(**kwargs)
        with open(file_metadata.path, "rb") as file:
            file_content = file.read()

        return file_metadata, file_content

    async def delete_image(
            self,
            payload: dict,
            **kwargs
    ):
        file_metadata: Image = await self.find(**kwargs)

        if not file_metadata :
            return False
        elif file_metadata.created_by != payload.get("user_id"):
            return False
        else:
            await self.delete_by_id(file_metadata.id)
            os.remove(file_metadata.path)
            return True




