from fastapi import APIRouter, Depends

from app.dependencies import (
    get_current_user,
    get_work_service
)
from app.schemas.works import WorksCreateRequestDTO
from app.services.work_service import WorkService

router = APIRouter(prefix='/works', tags=["works"])


@router.post("/")
async def create_works_controller(
        dto: WorksCreateRequestDTO,
        service: WorkService = Depends(get_work_service),
        _ = Depends(get_current_user)
):
    return await service.create_works(date=dto.date, work_days=dto.work_days)
