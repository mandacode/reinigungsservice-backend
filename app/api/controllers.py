import asyncio
import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from app.domain.models import User
from app.dtos import (
    EmployeeDTO,
    CustomerDTO,
    WorksCreateRequestDTO,
    InvoicesCreateDTO,
    UserLoginDTO,
    TokenDTO,
    UserDTO,
    UserRegisterDTO
)
from app.api.dependencies import (
    get_employee_service,
    get_customer_service,
    get_work_service,
    get_invoice_service,
    get_auth_service,
    get_current_user,
    get_seed_db_service,
    verify_admin_key
)
from app.config import settings
from app.services.auth_service import (
    TokenIsBlacklistedError,
    AuthService,
    UserAlreadyExistsError
)
from app.services.customer_service import CustomerService
from app.services.employee_service import EmployeeService
from app.services.invoices_service import CustomerInvoiceService
from app.services.seed_db_service import SeedDbService
from app.services.work_service import WorkService

router = APIRouter(prefix="/api")


@router.get("/employees", response_model=list[EmployeeDTO])
async def get_employees_controller(service: EmployeeService = Depends(get_employee_service)):
    return await service.get_all_employees()


@router.get("/customers", response_model=list[CustomerDTO])
async def get_customers_controller(service: CustomerService = Depends(get_customer_service)):
    return await service.get_all_customers()


@router.post("/works")
async def create_works_controller(
        dto: WorksCreateRequestDTO,
        service: WorkService = Depends(get_work_service)
):
    return await service.create_works(dto)


@router.post("/invoices")
async def create_invoices_controller(
        dto: InvoicesCreateDTO,
        service: CustomerInvoiceService = Depends(get_invoice_service)
):
    asyncio.create_task(
        service.generate_invoices(
            start_date=dto.start_date,
            end_date=dto.end_date,
            last_invoice_number=dto.last_invoice_number
        )
    )
    return {"message": "Invoice generation started in the background."}


@router.post("/auth/login", response_model=TokenDTO)
async def create_access_token_controller(creds: UserLoginDTO, service: AuthService = Depends(get_auth_service)):
    user = await service.authenticate(creds.username, creds.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = datetime.timedelta(minutes=settings.access_token_lifespan)
    access_token = service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "username": user.username
    }


@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, this is a protected route!"}


@router.post("/auth/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    service: AuthService = Depends(get_auth_service),
):
    token = credentials.credentials

    try:
        user = await service.get_current_user(token=token)
    except TokenIsBlacklistedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is blacklisted",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        await service.blacklist_token(token=token, user_id=user.id)
        return {"message": "Successfully logged out"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/auth/me", response_model=UserDTO)
async def get_current_user_info_controller(
    user: User = Depends(get_current_user)
):
    return user


@router.get("/health")
async def health_check_controller():
    return {"status": "ok", "message": "API is running"}


@router.post("/seed-db")
async def seed_db_controller(
        _ = Depends(verify_admin_key),
        service: SeedDbService = Depends(get_seed_db_service)
):
    await service.seed_db()
    return {"status": "ok", "message": "Database seeded successfully"}


@router.post("/auth/register")
async def register_admin_user_controller(
        data: UserRegisterDTO,
        _ = Depends(verify_admin_key),
        service: AuthService = Depends(get_auth_service)
):
    try:
        await service.register_user(username=data.username, password=data.password)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"status": "ok", "message": "User created"}
