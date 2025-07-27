import asyncio

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, create_invoice_task
from app.schemas.invoices import InvoicesCreateDTO


router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("/")
async def create_invoices_controller(
    dto: InvoicesCreateDTO,
    task: callable = Depends(create_invoice_task),
    _=Depends(get_current_user),
):
    asyncio.create_task(
        task(
            start_date=dto.start_date,
            end_date=dto.end_date,
            last_invoice_number=dto.last_invoice_number,
        )
    )
    return {"message": "Invoice generation started in the background."}
