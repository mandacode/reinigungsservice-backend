import json

from db.config import SessionLocal
from db.repositories import (
    EmployeeRepository,
    CustomerRepository,
    AddressRepository,
    BankAccountRepository
)
from db.tables import create_tables, run_mappers, reset_id_sequence
from domain.models import Employee, Address, BankAccount, Customer


def seed_db():

    with open('data/seed_dev.json', 'r') as file:
        data = json.load(file)

    create_tables()
    run_mappers()

    db = SessionLocal()
    try:

        employee_repo = EmployeeRepository(db)
        address_repo = AddressRepository(db)
        bank_account_repo = BankAccountRepository(db)
        customer_repo = CustomerRepository(db)

        employee_repo.delete_all()
        customer_repo.delete_all()
        address_repo.delete_all()
        bank_account_repo.delete_all()

        employees, customers, addresses, bank_accounts = [], [], [], []
        for item in data:

            if item['table'] == 'employees':
                employees.append(Employee(**item['fields']))

            elif item['table'] == 'addresses':
                addresses.append(Address(**item['fields']))

            elif item['table'] == 'bank_accounts':
                bank_accounts.append(BankAccount(**item['fields']))

            elif item['table'] == 'customers':
                customers.append(Customer(**item['fields']))

        if addresses:
            reset_id_sequence(db, 'addresses', 'id')
            address_repo.add_all(addresses)

        if bank_accounts:
            reset_id_sequence(db, 'bank_accounts', 'id')
            bank_account_repo.add_all(bank_accounts)

        if employees:
            reset_id_sequence(db, 'employees', 'id')
            employee_repo.add_all(employees)

        if customers:
            reset_id_sequence(db, 'customers', 'id')
            customer_repo.add_all(customers)

    except:
        db.rollback()
        print("An error occurred while seeding the database.")
        raise

    finally:
        db.close()

    print("Database seeded successfully.")


if __name__ == "__main__":
    seed_db()
