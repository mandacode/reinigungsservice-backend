from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.customer import Customer
from app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    _model = Customer

    async def get_all_with_addresses(self):
        stmt = (
            select(self._model)
            .options(selectinload(self._model.address))
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
