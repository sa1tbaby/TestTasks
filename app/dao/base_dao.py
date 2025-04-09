from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.database.metadata import DeclarativeBase
from app.dto.base_model import BaseModel

class BaseDao:
    def __init__(self, session: AsyncSession, model: DeclarativeBase):

        self.session: AsyncSession = session
        self.model: DeclarativeBase | None = model

    async def find(self, model: DeclarativeBase = None, **kwargs):
        if not model:
            model = self.model
        query = select(model).filter_by(**kwargs)
        result = await self.session.execute(query)
        result = result.scalars().first()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Not found",
            )

        return result

    async def find_by_id(self, model_id: int):
        query = select(self.model).where(self.model.id == model_id)
        result = await self.session.execute(query)

        return result.scalars().first()


    async def create_one(self, body: dict | BaseModel, model: DeclarativeBase = None):
        if not model:
            model = self.model
        model = model(**(body if isinstance(body, dict) else body.dict()))
        self.session.add(model)
        return model


    async def update_by_id(self, model_id: int, body):
        model = await self.find_by_id(model_id)
        self.__update_model_fields(model, body)
        return model


    async def delete_by_id(self, model_id: int):
        query = delete(self.model).where(self.model.id == model_id)
        await self.session.execute(query)


    def __update_model_fields(self, model, new_data):
        for key, value in new_data.dict().items():
            setattr(model, key, value)
