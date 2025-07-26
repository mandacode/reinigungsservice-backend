import datetime

from app.repositories.work_repository import WorkRepository


class WorkService:
    def __init__(self, work_repository: WorkRepository):
        self._work_repository = work_repository

    async def create_works(self, date: datetime.date, work_days: list) -> None:
        works = []
        for work_day in work_days:
            for work in work_day.works:
                works.append({
                    'customer_id': work.customer_id,
                    'employee_id': work_day.employee_id,
                    'date': date,
                    'hours': work.hours
                })

        if works:
            await self._work_repository.add_all(works)
