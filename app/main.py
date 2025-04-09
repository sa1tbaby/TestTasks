import uvicorn
from fastapi import FastAPI

from app.app_utils.bind_errors import bind_exceptions
from app.utils import bind_routes, bind_events
from app.handlers import routes
from app.settings import settings

import logging

logger = logging.getLogger(__name__)


def make_app() -> FastAPI:
    swagger_url = None
    openapi_url = None
    redoc_url = None

    if settings.SWAGGER_ENABLE:
        swagger_url = f"{settings.APP_URL_PREFIX}/swagger"
        openapi_url = f"{settings.APP_URL_PREFIX}/openapi.json"
        redoc_url = f"{settings.APP_URL_PREFIX}/redoc"

    app = FastAPI(
        title="Dr.Web Test",
        description="Dr.Web Test",
        docs_url=swagger_url,
        openapi_url=openapi_url,
        redoc_url=redoc_url,
    )

    bind_events(app, settings.database_url)
    bind_exceptions(app)
    bind_routes(app, routes)

    return app


if __name__ == "__main__":
    uvicorn.run(
        make_app(),
        port=settings.APP_PORT,
        host=settings.APP_HOST,
    )
