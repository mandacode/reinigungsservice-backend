from app.models.address import Address
from app.models.bank_account import BankAccount
from app.repositories import AddressRepository, BankAccountRepository
from app.repositories.employee_repository import EmployeeRepository
from app.models.employee import Employee
from app.schemas.employees import EmployeeCreateDTO


class EmployeeService:
    def __init__(
            self,
            employee_repository: EmployeeRepository,
            address_repository: AddressRepository,
            bank_account_repository: BankAccountRepository
    ):
        self._employee_repository = employee_repository
        self._address_repository = address_repository
        self._bank_account_repository = bank_account_repository

    async def get_all_employees(self) -> list[Employee]:
        return await self._employee_repository.get_all()

    async def create_employee(self, data: EmployeeCreateDTO) -> Employee:
        address = Address(
            street_address=data.address.street_address,
            city=data.address.city,
            postal_code=data.address.postal_code,
        )
        await self._address_repository.add(address)
        bank_account = BankAccount(
            bic=data.bank_account.bic,
            bank_name=data.bank_account.bank_name,
            iban=data.bank_account.iban,
        )
        await self._bank_account_repository.add(bank_account)
        employee = Employee(
            name=data.name,
            code=data.code,
            hourly_rate=data.hourly_rate,
            company_name=data.company_name,
            metadata=data.metadata,
        )
        employee.address = address
        employee.bank_account = bank_account
        return await self._employee_repository.add(employee)
