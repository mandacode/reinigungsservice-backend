from app.repositories.employee_repository import EmployeeRepository
from app.models.employee import Employee


class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository):
        self._employee_repository = employee_repository

    async def get_all_employees(self) -> list[Employee]:
        return await self._employee_repository.get_all()

    async def create_employee(self, data: dict) -> Employee:
        employee = Employee(**data)
        return await self._employee_repository.add(employee)
