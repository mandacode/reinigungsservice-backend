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
        self._repos = {
            "works": work_repository,
            "customers": customer_repository,
            "employees": employee_repository,
            "addresses": address_repository,
            "bank_accounts": bank_account_repository,
        }
        self._drive = drive

    async def seed_db(self) -> None:
        for repo in  self._repos.values():
            await repo.delete_all()

        now = datetime.datetime.now()
        data = await self._drive.download(settings.seed_file_id)

        entities = {
            "addresses": [],
            "bank_accounts": [],
            "employees": [],
            "customers": [],
        }

        for item in data:
            item["fields"]["created_at"] = item["fields"]["updated_at"] = now
            entities.get(item["table"], []).append(item["fields"])

        for entity_name, entity_data in entities.items():
            if not entity_data:
                continue
            repo = self._repos[entity_name]
            session = repo.get_session()
            await reset_id_sequence(session, entity_name, "id")
            await repo.add_all(entity_data)

    print("Database seeded successfully.")
