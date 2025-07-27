import datetime

from app.repositories.customer_repository import CustomerRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.work_repository import WorkRepository
from app.repositories import AddressRepository, BankAccountRepository

from app.database.orm import reset_id_sequence
from app.services.google_drive_service import GoogleDriveAsyncService
from app.config import settings


class SeedDbService:
    def __init__(
        self,
        customer_repository: CustomerRepository,
        employee_repository: EmployeeRepository,
        work_repository: WorkRepository,
        address_repository: AddressRepository,
        bank_account_repository: BankAccountRepository,
        drive: GoogleDriveAsyncService,
    ):
        self._customer_repository = customer_repository
        self._employee_repository = employee_repository
        self._work_repository = work_repository
        self._address_repository = address_repository
        self._bank_account_repository = bank_account_repository
        self._drive = drive

    async def seed_db(self) -> None:
        repos = (
            self._work_repository,
            self._customer_repository,
            self._employee_repository,
            self._address_repository,
            self._bank_account_repository,
        )
        for repo in repos:
            await repo.delete_all()

        now = datetime.datetime.now()

        data = await self._drive.download(settings.seed_file_id)

        employees, customers, addresses, bank_accounts = [], [], [], []
        for item in data:
            item["fields"]["created_at"] = item["fields"]["updated_at"] = now

            if item["table"] == "employees":
                employees.append(item["fields"])

            elif item["table"] == "addresses":
                addresses.append(item["fields"])

            elif item["table"] == "bank_accounts":
                bank_accounts.append(item["fields"])

            elif item["table"] == "customers":
                customers.append(item["fields"])

        if addresses:
            session = self._address_repository.get_session()
            await reset_id_sequence(session, "addresses", "id")
            await self._address_repository.add_all(addresses)

        if bank_accounts:
            session = self._bank_account_repository.get_session()
            await reset_id_sequence(session, "bank_accounts", "id")
            await self._bank_account_repository.add_all(bank_accounts)

        if employees:
            session = self._employee_repository.get_session()
            await reset_id_sequence(session, "employees", "id")
            await self._employee_repository.add_all(employees)

        if customers:
            session = self._customer_repository.get_session()
            await reset_id_sequence(session, "customers", "id")
            await self._customer_repository.add_all(customers)

    print("Database seeded successfully.")
