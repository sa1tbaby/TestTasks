from app.dto.base_model import BaseModel

class ImageDto(BaseModel):
    file_name_hash: str

class ImageReprDto(BaseModel):
    __model__ = "Image"

    name: str
    name_hash: str
    path: str
    type: str
    content: bytes







