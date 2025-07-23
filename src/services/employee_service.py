from db.repositories import EmployeeRepository
from domain.models import Employee


class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository):
        self._employee_repository = employee_repository

    async def get_all_employees(self) -> list[Employee]:
        return await self._employee_repository.get_all()
