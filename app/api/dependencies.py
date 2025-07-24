import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.db.config import get_session
from app.db.repositories import EmployeeRepository, CustomerRepository, WorkRepository, UserRepository, BlacklistedTokenRepository
from app.services.employee_service import EmployeeService
from app.services.customer_service import CustomerService
from app.services.work_service import WorkService
from app.services.invoices_service import CustomerInvoiceService
from app.services.google_drive_service import GoogleDriveAsyncService
from app.services.auth_service import AuthService, TokenIsBlacklistedError
from app.domain.models import User


def get_employee_repository(db=Depends(get_session)) -> EmployeeRepository:
    return EmployeeRepository(db)

def get_employee_service(employee_repository: EmployeeRepository = Depends(get_employee_repository)) -> EmployeeService:
    return EmployeeService(employee_repository=employee_repository)

def get_customer_repository(db=Depends(get_session)) -> CustomerRepository:
    return CustomerRepository(db)

def get_customer_service(customer_repository: CustomerRepository = Depends(get_customer_repository)) -> CustomerService:
    return CustomerService(customer_repository=customer_repository)

def get_work_repository(db=Depends(get_session)) -> WorkRepository:
    return WorkRepository(db)

def get_work_service(work_repository: WorkRepository = Depends(get_work_repository)) -> WorkService:
    return WorkService(work_repository=work_repository)

def get_google_drive_service() -> GoogleDriveAsyncService:
    return GoogleDriveAsyncService.from_base64(
        creds_b64=os.getenv("GOOGLE_API_CREDENTIALS_B64")
    )

def get_invoice_service(
        drive: GoogleDriveAsyncService = Depends(get_google_drive_service),
        employee_repository: EmployeeRepository = Depends(get_employee_repository),
        customer_repository: CustomerRepository = Depends(get_customer_repository),
        work_repository: WorkRepository = Depends(get_work_repository)
) -> CustomerInvoiceService:
    return CustomerInvoiceService(
        drive=drive,
        employee_repository=employee_repository,
        customer_repository=customer_repository,
        work_repository=work_repository
    )

def get_user_repository(db=Depends(get_session)):
    return UserRepository(db)

def get_blacklisted_tokens_repository(db=Depends(get_session)):
    return BlacklistedTokenRepository(db)

def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        blacklisted_token_repository: BlacklistedTokenRepository = Depends(get_blacklisted_tokens_repository)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        blacklisted_token_repository=blacklisted_token_repository
    )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    service = Depends(get_auth_service)
) -> User:
    try:
        current_user = await service.get_current_user(credentials.credentials)
        return current_user
    except TokenIsBlacklistedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is blacklisted",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
