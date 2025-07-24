import asyncio
import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from dtos import (
    EmployeeDTO, CustomerDTO, WorksCreateRequestDTO, InvoicesCreateDTO, UserLoginDTO, TokenDTO, UserDTO
)
from api.dependencies import (
    get_employee_service,
    get_customer_service,
    get_work_service,
    get_invoice_service,
    get_auth_service,
    get_current_user
)
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from services.auth_service import TokenIsBlacklistedError

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


@router.post("/auth/login", response_model=TokenDTO)
async def login(creds: UserLoginDTO, service = Depends(get_auth_service)):
    user = await service.authenticate(creds.username, creds.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "username": user.username
    }


@router.get("/protected")
async def protected_route(current_user = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, this is a protected route!"}


@router.post("/auth/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    service = Depends(get_auth_service),
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
async def get_current_user_info(
    user = Depends(get_current_user)
):
    return user


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running"}

