import asyncio

from fastapi import APIRouter, Depends

from dtos import EmployeeDTO, CustomerDTO, WorksCreateRequestDTO, InvoicesCreateDTO
from api.dependencies import (
    get_employee_service,
    get_customer_service,
    get_work_service,
    get_invoice_service
)


router = APIRouter(prefix="/api")


@router.get("/employees", response_model=list[EmployeeDTO])
async def get_employees_controller(service = Depends(get_employee_service)):
    return await service.get_all_employees()


@router.get("/customers", response_model=list[CustomerDTO])
async def get_customers_controller(service = Depends(get_customer_service)):
    return await service.get_all_customers()


@router.post("/works")
async def create_works_controller(
        dto: WorksCreateRequestDTO,
        service = Depends(get_work_service)
):
    return await service.create_works(dto)


@router.post("/invoices")
async def create_invoices_controller(
        dto: InvoicesCreateDTO,
        service = Depends(get_invoice_service)
):
    asyncio.create_task(
        service.generate_invoices(
            start_date=dto.start_date,
            end_date=dto.end_date,
            last_invoice_number=dto.last_invoice_number
        )
    )
    return {"message": "Invoice generation started in the background."}