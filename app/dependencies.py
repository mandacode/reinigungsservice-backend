import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import get_session, async_session
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.work_repository import WorkRepository
from app.repositories import AddressRepository, BankAccountRepository
from app.repositories.user_repository import UserRepository
from app.repositories.blacklisted_token_repository import BlacklistedTokenRepository
from app.services.employee_service import EmployeeService
from app.services.customer_service import CustomerService
from app.services.work_service import WorkService
from app.services.invoices_service import CustomerInvoiceService
from app.services.google_drive_service import GoogleDriveAsyncService
from app.services.auth_service import AuthService, TokenIsBlacklistedError
from app.services.seed_db_service import SeedDbService
from app.models.user import User
from app.config import settings


# Services
def get_employee_service(
    session: AsyncSession = Depends(get_session),
) -> EmployeeService:
    return EmployeeService(
        employee_repository=EmployeeRepository(session),
        address_repository=AddressRepository(session),
        bank_account_repository=BankAccountRepository(session),
    )


def get_customer_service(
    session: AsyncSession = Depends(get_session),
) -> CustomerService:
    return CustomerService(
        customer_repository=CustomerRepository(session),
        address_repository=AddressRepository(session),
    )


def get_work_service(
    session: AsyncSession = Depends(get_session),
) -> WorkService:
    return WorkService(work_repository=WorkRepository(session))


def get_google_drive_service() -> GoogleDriveAsyncService:
    return GoogleDriveAsyncService.from_base64(
        creds_b64=os.getenv("GOOGLE_API_CREDENTIALS_B64")
    )


def get_invoice_service(
    drive: GoogleDriveAsyncService = Depends(get_google_drive_service),
    session: AsyncSession = Depends(get_session),
) -> CustomerInvoiceService:
    return CustomerInvoiceService(
        drive=drive,
        employee_repository=EmployeeRepository(session),
        customer_repository=CustomerRepository(session),
        work_repository=WorkRepository(session),
    )


def get_auth_service(
    session: AsyncSession = Depends(get_session),
) -> AuthService:
    return AuthService(
        user_repository=UserRepository(session),
        blacklisted_token_repository=BlacklistedTokenRepository(session),
    )


async def get_seed_db_service(
    drive: GoogleDriveAsyncService = Depends(get_google_drive_service),
    session: AsyncSession = Depends(get_session),
) -> SeedDbService:
    return SeedDbService(
        drive=drive,
        address_repository=AddressRepository(session),
        bank_account_repository=BankAccountRepository(session),
        employee_repository=EmployeeRepository(session),
        customer_repository=CustomerRepository(session),
        work_repository=WorkRepository(session),
    )


# Authentication and Authorization
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    service=Depends(get_auth_service),
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


async def verify_admin_key(
    admin_key: str = Depends(APIKeyHeader(name="admin_key", auto_error=False)),
):
    if admin_key != settings.admin_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin key"
        )


async def create_invoice_task(
    drive: GoogleDriveAsyncService = Depends(get_google_drive_service),
) -> callable:
    async def task(start_date: str, end_date: str, last_invoice_number: int):
        async with async_session() as session:
            service = CustomerInvoiceService(
                drive=drive,
                employee_repository=EmployeeRepository(session),
                customer_repository=CustomerRepository(session),
                work_repository=WorkRepository(session),
            )
            await service.generate_invoices(
                start_date=start_date,
                end_date=end_date,
                last_invoice_number=last_invoice_number,
            )

    return task
