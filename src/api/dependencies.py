import os

from fastapi import Depends

from db.config import get_session
from db.repositories import EmployeeRepository, CustomerRepository, WorkRepository
from services.employee_service import EmployeeService
from services.customer_service import CustomerService
from services.work_service import WorkService
from services.invoices_service import CustomerInvoiceService
from services.google_drive_service import GoogleDriveAsyncService


def get_employee_repository(db=Depends(get_session)) -> EmployeeRepository:
    return EmployeeRepository(db)

def get_employee_service(repo: EmployeeRepository = Depends(get_employee_repository)) -> EmployeeService:
    return EmployeeService(repo)

def get_customer_repository(db=Depends(get_session)) -> CustomerRepository:
    return CustomerRepository(db)

def get_customer_service(repo: CustomerRepository = Depends(get_customer_repository)) -> CustomerService:
    return CustomerService(repo)

def get_work_repository(db=Depends(get_session)) -> WorkRepository:
    return WorkRepository(db)

def get_work_service(repo: WorkRepository = Depends(get_work_repository)) -> WorkService:
    return WorkService(repo)

def get_google_drive_service() -> GoogleDriveAsyncService:
    return GoogleDriveAsyncService.from_base64(
        creds_b64=os.getenv("GOOGLE_API_CREDENTIALS_B64")
    )

def get_invoice_service(
        drive: GoogleDriveAsyncService = Depends(get_google_drive_service),
        employee_repo: EmployeeRepository = Depends(get_employee_repository),
        customer_repo: CustomerRepository = Depends(get_customer_repository),
        work_repo: WorkRepository = Depends(get_work_repository)
) -> CustomerInvoiceService:
    return CustomerInvoiceService(
        drive=drive,
        employee_repo=employee_repo,
        customer_repo=customer_repo,
        work_repo=work_repo
    )
