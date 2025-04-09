from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from asgi_lifespan import LifespanManager
import pytest
import pytest_asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock

from app.app_utils.jwt import JWT
from app.database.metadata import DeclarativeBase
from app.models import User
from app.settings import settings
from pydantic import BaseModel as PydanticBaseModel

from tests.test_dto import AuthBody


@pytest_asyncio.fixture(scope="session")
async def _app() -> FastAPI:
    from app.main import make_app
    app = make_app()
    async with LifespanManager(app):  # Активируем lifespan
        yield app


@pytest_asyncio.fixture(scope="session")
async def _client(_app: FastAPI) -> AsyncClient:
    transport = ASGITransport(_app)
    async with AsyncClient(base_url="http://localhost:8001", transport=transport) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def _async_session_maker():
    """Mock async_sessionmaker in sqlalchemy.ext.asyncio."""
    with patch(
            target="sqlalchemy.ext.asyncio.async_sessionmaker",
            new=MagicMock,
            spec=async_sessionmaker
    ) as mock:
        yield mock


@pytest.fixture(scope="session", autouse=True)
def _create_async_engine():
    """Mock create_async_engine in sqlalchemy.ext.asyncio."""
    with patch(
            target="sqlalchemy.ext.asyncio.create_async_engine",
            new=MagicMock,
            spec=AsyncEngine
    ) as mock:
        yield mock


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _async_session():
    """Mock AsyncSession in sqlalchemy.ext.asyncio.AsyncSession"""
    with patch("sqlalchemy.ext.asyncio.AsyncSession") as mock:
        yield mock


@pytest.fixture(scope="session", autouse=True)
def mock_get_master_session(_async_session):
    """Mock get_master_session in app.database.accessor.PostgresAccessor"""
    with patch(
        target="app.database.PostgresAccessor.get_master_session",
        new=MagicMock
    ) as mock:
        _mock = AsyncMock()
        _mock.__aenter__.return_value = _async_session
        _mock.__aexit__.return_value = None
        mock.return_value = _mock
        yield mock


@pytest.fixture(scope="session", autouse=True)
def storage_dir():
    """Creates and cleans up a temporary storage directory for tests."""
    import os
    import shutil
    storage_dir = settings.STORE_PATH
    os.makedirs(storage_dir, exist_ok=True)
    yield storage_dir
    shutil.rmtree(storage_dir)


@pytest.fixture()
def mock_factory_for_find(mocker):
    """Fabric for method app.dao.BaseDao.find"""
    def apply_mock(model: DeclarativeBase, target: str, **kwargs):
        from app import models
        if not model.__name__ in models.__all__:
            raise ValueError(f"Model {model} doesnt support cause not found in app.models")

        _mock = MagicMock(spec=model)
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(_mock, key, value)

        mocker.patch(target=target, return_value=_mock)

    return apply_mock


@pytest.fixture(scope="session")
def mock_body():
    def apply_mock(model: PydanticBaseModel, **kwargs):
        return model(**kwargs)
    return apply_mock