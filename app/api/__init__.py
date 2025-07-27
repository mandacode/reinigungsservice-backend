from fastapi import APIRouter, Depends

from app.dependencies import verify_admin_key, get_seed_db_service
from app.services.seed_db_service import SeedDbService
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.invoices import router as invoices_router
from app.api.endpoints.works import router as works_router
from app.api.endpoints.employees import router as employees_router
from app.api.endpoints.customers import router as customers_router


router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(invoices_router)
router.include_router(works_router)
router.include_router(employees_router)
router.include_router(customers_router)


@router.post("/seed-db")
async def seed_db_controller(
    _=Depends(verify_admin_key), service: SeedDbService = Depends(get_seed_db_service)
):
    await service.seed_db()
    return {"status": "ok", "message": "Database seeded successfully"}


@router.get("/health")
async def health_check_controller():
    return {"status": "ok", "message": "API is running"}
