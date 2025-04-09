from app.settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str | None = "localhost"
    DB_PORT: str | None = "5432"
    DB_USER: str | None = "pgadmin"
    DB_PASSWORD: str | None = "pgadmin"
    DB_NAME: str | None = "local-db"

    APP_HOST: str | None = "localhost"
    APP_PORT: int | None = 8001

    TOKEN_ACCESS: str | None = "access_token"
    TOKEN_EXPIRES_MINUTES: int | None = 60 * 24
    TOKEN_ALGORITHM: str | None = "HS256"
    TOKEN_SECRET_KEY: str | None = "eyJhbGciOiJIUzI1NiJ9.ew0KICAic3ViIjogIjEyMzQ1Njc4OTAiLA0KICAibmFtZSI6ICJBbmlzaCBOYXRoIiwNCiAgImlhdCI6IDE1MTYyMzkwMjINCn0.b1kJBUrm71hZKqz6VCQXN_6je82v0dZuyHmaKtYlGPU"

    STORE_PATH: str | None = "store"
    SWAGGER_ENABLE: bool | None = True

