from app.dto.base_model import BaseModel

class TokenPayload(BaseModel):
    user_id: int
    user_name: str


