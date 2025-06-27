from fastapi import Depends

from db.config import get_db
from db.repositories import EmployeeRepository, CustomerRepository, WorkRepository
from services.employee_service import EmployeeService
from services.customer_service import CustomerService
from services.work_service import WorkService


def get_employee_repository(db=Depends(get_db)) -> EmployeeRepository:
    return EmployeeRepository(db)

def get_employee_service(repo: EmployeeRepository = Depends(get_employee_repository)) -> EmployeeService:
    return EmployeeService(repo)

def get_customer_repository(db=Depends(get_db)) -> CustomerRepository:
    return CustomerRepository(db)

def get_customer_service(repo: CustomerRepository = Depends(get_customer_repository)) -> CustomerService:
    return CustomerService(repo)

def get_work_repository(db=Depends(get_db)) -> WorkRepository:
    return WorkRepository(db)

def get_work_service(repo: WorkRepository = Depends(get_work_repository)) -> WorkService:
    return WorkService(repo)
