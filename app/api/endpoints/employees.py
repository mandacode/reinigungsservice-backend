from fastapi import APIRouter, Depends

from app.dependencies import (
    get_current_user,
    get_employee_service,
)
from app.schemas.works import EmployeeDTO
from app.services.employee_service import EmployeeService

router = APIRouter(prefix='/employees', tags=["employees"])


@router.get("/", response_model=list[EmployeeDTO])
async def get_employees_controller(
        service: EmployeeService = Depends(get_employee_service),
        _ = Depends(get_current_user)
):
    return await service.get_all_employees()
