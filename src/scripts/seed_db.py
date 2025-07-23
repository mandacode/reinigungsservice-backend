import asyncio
import datetime

from db.config import async_session, engine
from db.repositories import (
    EmployeeRepository,
    CustomerRepository,
    AddressRepository,
    BankAccountRepository,
    WorkRepository
)
from db.tables import create_tables, run_mappers, reset_id_sequence
from services.google_drive_service import GoogleDriveAsyncService

from config import SEED_FILE_ID, GOOGLE_API_CREDENTIALS_B64



async def seed_db():
    service = GoogleDriveAsyncService.from_base64(GOOGLE_API_CREDENTIALS_B64)
    data = await service.download(SEED_FILE_ID)

    await create_tables(engine=engine)
    run_mappers()

    async with async_session() as db:

        employee_repo = EmployeeRepository(db)
        address_repo = AddressRepository(db)
        bank_account_repo = BankAccountRepository(db)
        customer_repo = CustomerRepository(db)
        works_repo = WorkRepository(db)

        await works_repo.delete_all()
        await employee_repo.delete_all()
        await customer_repo.delete_all()
        await address_repo.delete_all()
        await bank_account_repo.delete_all()

        now = datetime.datetime.now()

        employees, customers, addresses, bank_accounts = [], [], [], []
        for item in data:

            item['fields']['created_at'] = item['fields']['updated_at'] = now

            if item['table'] == 'employees':
                employees.append(item['fields'])

            elif item['table'] == 'addresses':
                addresses.append(item['fields'])

            elif item['table'] == 'bank_accounts':
                bank_accounts.append(item['fields'])

            elif item['table'] == 'customers':
                customers.append(item['fields'])

        if addresses:
            await reset_id_sequence(db, 'addresses', 'id')
            await address_repo.add_all(addresses)

        if bank_accounts:
            await reset_id_sequence(db, 'bank_accounts', 'id')
            await bank_account_repo.add_all(bank_accounts)

        if employees:
            await reset_id_sequence(db, 'employees', 'id')
            await employee_repo.add_all(employees)

        if customers:
            await reset_id_sequence(db, 'customers', 'id')
            await customer_repo.add_all(customers)

    print("Database seeded successfully.")


if __name__ == "__main__":
    asyncio.run(seed_db())
