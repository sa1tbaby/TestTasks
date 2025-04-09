from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from typing import AsyncGenerator
from contextlib import asynccontextmanager

class PostgresAccessor:
    def __init__(self, db_url: str):
        self.engine: AsyncEngine | None = None
        self.session_maker: async_sessionmaker[AsyncSession] | None = None
        if not db_url:
            raise ValueError("Expected database url")
        self.DB_URL: str = db_url

    async def set_engine(self) -> None:
        self.engine = create_async_engine(
            self.DB_URL,
            echo=False,
            pool_pre_ping=True
        )
        self.session_maker = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

    async def stop(self) -> None:
        await self.engine.dispose()

    @asynccontextmanager
    async def get_master_session(self) -> AsyncGenerator[AsyncSession, None]:
        if self.session_maker:
            async with self.session_maker.begin() as session:  # pylint: disable=no-member
                yield session
        else:
            raise ValueError("Session maker is not initialized.")
