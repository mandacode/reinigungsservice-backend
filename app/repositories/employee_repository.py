from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.employee import Employee
from app.repositories.base_repository import BaseRepository


class EmployeeRepository(BaseRepository):
    _model = Employee

    async def get_by_code(self, code: str) -> Employee:
        stmt = (
            select(
                self._model
            )
            .options(
                selectinload(self._model.address),
                selectinload(self._model.bank_account)
            )
            .where(self._model.code == code)
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()
