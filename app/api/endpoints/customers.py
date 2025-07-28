from fastapi import APIRouter, Depends

from app.dependencies import (
    get_current_user,
    get_customer_service,
)
from app.schemas.customers import CustomerDTO, CustomerCreateDTO
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=list[CustomerDTO])
async def get_customers_controller(
    service: CustomerService = Depends(get_customer_service),
    _=Depends(get_current_user),
):
    return await service.get_all_customers()


@router.post("/", response_model=CustomerDTO)
async def create_customer_controller(
    data: CustomerCreateDTO,
    service: CustomerService = Depends(get_customer_service),
    _=Depends(get_current_user),
):
    return await service.create_customer(data)
