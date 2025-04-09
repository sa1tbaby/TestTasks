from fastapi import APIRouter, FastAPI
from app.settings import env, settings

from app.database import PostgresAccessor


def bind_routes(app: FastAPI, routes: list[APIRouter]):
    for route in routes:
        app.include_router(route, prefix=settings.APP_URL_PREFIX)

def bind_events(
        app: FastAPI,
        db_url: str,
) -> None:
    @app.on_event("startup")
    async def set_engine():
        db = PostgresAccessor(db_url=db_url)
        await db.set_engine()
        app.state.db = db

    @app.on_event("shutdown")
    async def close_engine():
        await app.state.db.stop()
