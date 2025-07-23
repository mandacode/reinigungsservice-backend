from db.repositories import WorkRepository
from dtos import WorksCreateRequestDTO


class WorkService:
    def __init__(self, work_repository: WorkRepository):
        self._work_repository = work_repository

    async def create_works(self, data: WorksCreateRequestDTO) -> None:
        works = []
        for work_day in data.work_days:
            for work in work_day.works:
                works.append({
                    'customer_id': work.customer_id,
                    'employee_id': work_day.employee_id,
                    'date': data.date,
                    'hours': work.hours
                })

        if works:
            await self._work_repository.add_all(works)
