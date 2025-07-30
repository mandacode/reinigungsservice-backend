from typing import Generic, TypeVar

from sqlalchemy import select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base_model import BaseModel


Model = TypeVar("Model", bound=BaseModel)


class BaseRepository(Generic[Model]):
    _model: Model

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Model]:
        result = await self._session.execute(select(self._model))
        return result.scalars().all()

    async def add_all(self, entities: list[dict]) -> None:
        await self._session.execute(insert(self._model), entities)
        await self._session.commit()

    async def delete_all(self) -> None:
        await self._session.execute(delete(self._model))
        await self._session.commit()

    async def add(self, entity: Model) -> Model:
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def delete(self, entity: Model) -> None:
        await self._session.delete(entity)
        await self._session.commit()

    async def get(self, entity_id: int) -> Model | None:
        stmt = select(self._model).where(self._model.id == entity_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    def get_session(self) -> AsyncSession:
        return self._session
