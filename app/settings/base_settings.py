from pydantic import BaseSettings as PydanticBaseSettings

from app.settings import env


class BaseSettings(PydanticBaseSettings):
    DB_HOST: str | None
    DB_PORT: str | None
    DB_USER: str | None
    DB_PASSWORD: str | None
    DB_NAME: str | None

    APP_HOST: str | None
    APP_PORT: int | None
    APP_URL_PREFIX: str | None = f"/{env}/api/v1"

    TOKEN_ACCESS: str | None
    TOKEN_EXPIRES_MINUTES: int | None
    TOKEN_ALGORITHM: str | None = "HS256"
    TOKEN_SECRET_KEY: str | None

    STORE_PATH: str | None
    SWAGGER_ENABLE: bool | None = True

    @property
    def database(self):
        return {
            "database": self.DB_NAME,
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "host": self.DB_HOST,
            "port": self.DB_PORT,
        }

    @property
    def token(self):
        return {
            "access_token": self.TOKEN_ACCESS,
            "expires_minutes": self.TOKEN_EXPIRES_MINUTES,
            "algorithm": self.TOKEN_ALGORITHM,
            "secret_key": self.TOKEN_SECRET_KEY,
        }

    @property
    def app(self):
        return {
            "host": self.APP_HOST,
            "port": self.APP_PORT,
            "url_prefix": self.APP_URL_PREFIX
        }

    @property
    def database_url(self):
        return (
            "postgresql+asyncpg://"
            "{user}:{password}@{host}:{port}"
            "/{database}?ssl=require".format(**self.database)
        )

    @property
    def application_url(self):
        return "http://{host}:{port}".format(**self.app)

    @property
    def base_url(self):
        return "http://{host}:{port}{url_prefix}"

    @property
    def app_name(self):
        for part in reversed(self.APP_URL_PREFIX.split('/')):
            if part:
                return part
