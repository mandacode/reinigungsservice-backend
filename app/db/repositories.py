from typing import Generic, TypeVar
import datetime

from sqlalchemy import select, delete, insert, func
from sqlalchemy.orm import selectinload

from app.domain.models import (
    Employee,
    Customer,
    Address,
    BankAccount,
    Work,
    BaseModel,
    User,
    BlacklistedToken
)


Model = TypeVar('Model', bound=BaseModel)


class BaseRepository(Generic[Model]):
    _model: Model

    def __init__(self, session):
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

    async def add(self, entity: Model) -> None:
        self._session.add(entity)
        await self._session.commit()

    async def delete(self, entity: Model) -> None:
        await self._session.delete(entity)
        await self._session.commit()


class EmployeeRepository(BaseRepository):
    _model = Employee

    async def get_by_code(self, code: str) -> Model | None:
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


class CustomerRepository(BaseRepository):
    _model = Customer

    async def get_all_with_addresses(self):
        stmt = (
            select(self._model)
            .options(selectinload(self._model.address))
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

class AddressRepository(BaseRepository):
    _model = Address


class BankAccountRepository(BaseRepository):
    _model = BankAccount


class WorkRepository(BaseRepository):
    _model = Work

    async def get_by_period(self, start_date: datetime.date, end_date: datetime.date):
        stmt = (
            select(
                self._model.customer_id,
                self._model.date,
                Customer.hourly_rate,
                func.sum(self._model.hours).label('total_hours'),
                func.sum(self._model.hours * Customer.hourly_rate).label('total_price')
            )
            .join(
                Customer, self._model.customer_id == Customer.id
            )
            .where(
                self._model.date >= start_date,
                self._model.date <= end_date
            )
            .group_by(self._model.customer_id, self._model.date, Customer.hourly_rate)
            .order_by(self._model.customer_id, self._model.date)
        )
        result = await self._session.execute(stmt)
        return result.all()


class UserRepository(BaseRepository):
    _model = User

    async def get_by_username(self, username: str) -> bool:
        stmt = select(self._model).where(self._model.username == username)
        result = await self._session.execute(stmt)
        return result.scalars().first()


class BlacklistedTokenRepository(BaseRepository):
    _model = BlacklistedToken

    async def is_blacklisted(self, token: str) -> bool:
        stmt = select(self._model).where(self._model.token == token)
        result = await self._session.execute(stmt)
        return result.scalars().first() is not None
