import logging
from datetime import datetime, timedelta

from fastapi.security import HTTPBasic
from jose import jwt
from passlib.context import CryptContext
from fastapi import Response
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request


from app.settings import settings, env as app_env


class JWT:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    security = HTTPBasic()

    @staticmethod
    async def authorization(request: Request) -> dict:
        if isinstance(request, Response):
            msg = ("method JWT.authorization should by used with Request obj "
                   "using this method with Response obj should be only in test cases")
            if app_env == "local":
                logging.warning(msg)
            else:
                logging.error(msg)
                raise ValueError("WRONG request type in JWT.authorization")

        token = request.cookies.get(settings.TOKEN_ACCESS)
        payload = JWT.validate_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    @classmethod
    def create_token(cls, data: dict, expires_delta: timedelta | None = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRES_MINUTES)

        _data = data.copy()
        _data.update({"exp": expire})
        return jwt.encode(_data, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)

    @classmethod
    def validate_token(cls, token: str) -> dict | bool:
        try:
            payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
            if not payload.get("user_id") and not payload.get("user_name"):
                return False
        except Exception as exc:
            logging.error("Validate error", exc_info=exc)
            return False
        else:
            return payload

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)
