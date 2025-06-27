from db.repositories import WorkRepository
from domain.models import Work
from dtos import WorksCreateRequestDTO


class WorkService:
    def __init__(self, work_repository: WorkRepository):
        self._work_repository = work_repository

    def create_works(self, data: WorksCreateRequestDTO) -> None:
        works = []
        for work_day in data.work_days:
            employee_id = work_day.employee_id

            for work in work_day.works:
                customer_id = work.customer_id
                hours = work.hours

                work = Work(
                    customer_id=customer_id,
                    employee_id=employee_id,
                    date=data.date,
                    hours=hours
                )
                works.append(work)

        if works:
            self._work_repository.add_all(works)
