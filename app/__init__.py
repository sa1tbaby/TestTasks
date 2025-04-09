__version__ = "1.0.0"

from functools import lru_cache

from app.settings import Settings


@lru_cache
def get_settings():
    settings = Settings()
    settings.DB_URI_ALEMBIC = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    return settings