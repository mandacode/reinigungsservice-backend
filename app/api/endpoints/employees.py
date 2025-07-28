from fastapi import APIRouter, Depends

from app.dependencies import (
    get_current_user,
    get_employee_service,
)
from app.schemas.employees import EmployeeDTO, EmployeeCreateDTO
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=list[EmployeeDTO])
async def get_employees_controller(
    service: EmployeeService = Depends(get_employee_service),
    _=Depends(get_current_user),
):
    return await service.get_all_employees()


@router.post("/", response_model=EmployeeDTO)
async def create_employee_controller(
    data: EmployeeCreateDTO,
    service: EmployeeService = Depends(get_employee_service),
    _=Depends(get_current_user),
):
    return await service.create_employee(data)
