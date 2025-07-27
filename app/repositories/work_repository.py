import datetime

from sqlalchemy import select, func

from app.models.work import Work
from app.models.customer import Customer
from app.repositories.base_repository import BaseRepository


class WorkRepository(BaseRepository):
    _model = Work

    async def get_by_period(self, start_date: datetime.date, end_date: datetime.date):
        stmt = (
            select(
                self._model.customer_id,
                self._model.date,
                Customer.hourly_rate,
                func.sum(self._model.hours).label("total_hours"),
                func.sum(self._model.hours * Customer.hourly_rate).label("total_price"),
            )
            .join(Customer, self._model.customer_id == Customer.id)
            .where(self._model.date >= start_date, self._model.date <= end_date)
            .group_by(self._model.customer_id, self._model.date, Customer.hourly_rate)
            .order_by(self._model.customer_id, self._model.date)
        )
        result = await self._session.execute(stmt)
        return result.all()
