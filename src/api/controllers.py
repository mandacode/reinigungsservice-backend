from fastapi import APIRouter, Depends

from dtos import EmployeeDTO, CustomerDTO, WorksCreateRequestDTO
from api.dependencies import (
    get_employee_service, get_customer_service, get_work_service
)


router = APIRouter(prefix="/api")


@router.get("/employees", response_model=list[EmployeeDTO])
def get_employees_controller(service = Depends(get_employee_service)):
    return service.get_all_employees()


@router.get("/customers", response_model=list[CustomerDTO])
def get_customers_controller(service = Depends(get_customer_service)):
    return service.get_all_customers()


@router.post("/works")
def create_works_controller(
        dto: WorksCreateRequestDTO,
        service = Depends(get_work_service)
):
    return service.create_works(dto)
