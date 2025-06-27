from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    DECIMAL,
    JSON,
    MetaData,
    Date,
    func, text
)
from sqlalchemy.orm import registry, relationship

from domain.models import Employee, Customer, Work, Address, BankAccount

from db.config import engine

mapper_registry = registry()
metadata = MetaData()

addresses_table = Table(
    "addresses", metadata,
    Column("id", Integer, primary_key=True),
    Column("street_address", String(100), nullable=False),
    Column("postal_code", String(6), nullable=False),
    Column("city", String(50), nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)


bank_accounts_table = Table(
    "bank_accounts", metadata,
    Column("id", Integer, primary_key=True),
    Column("iban", String(40), nullable=False),
    Column("bank_name", String(100), nullable=False),
    Column("bic", String(11), nullable=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)

employees_table = Table(
    "employees", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False, index=True),
    Column("code", String(2), nullable=False, index=True),
    Column("hourly_rate", DECIMAL(4, 2), nullable=False, default=12.00),
    Column("company_name", String(100), nullable=True),
    Column("metadata", JSON, default=dict),
    Column("address_id", ForeignKey("addresses.id"), nullable=True),
    Column("bank_account_id", ForeignKey("bank_accounts.id"), nullable=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)


customers_table = Table(
    "customers", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False, index=True),
    Column("metadata", JSON, default=dict),
    Column("invoice_name", String(200), nullable=True),
    Column("hourly_rate", DECIMAL(4, 2), default=0.00),
    Column("note", String(500), nullable=True),
    Column("address_id", ForeignKey("addresses.id"), nullable=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)


works_table = Table(
    "works", metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", ForeignKey("customers.id"), nullable=False),
    Column("employee_id", ForeignKey("employees.id"), nullable=False),
    Column("hours", DECIMAL(5, 2), nullable=False),
    Column("date", Date, index=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(),
           onupdate=func.now()),
)



def run_mappers():
    mapper_registry.map_imperatively(Address, addresses_table, properties={
        "employees": relationship("Employee", backref="address"),
        "customers": relationship("Customer", backref="address"),
    })

    mapper_registry.map_imperatively(
        BankAccount, bank_accounts_table, properties={
            "employees": relationship("Employee", backref="bank_account")}
    )

    mapper_registry.map_imperatively(Employee, employees_table, properties={
        "works": relationship("Work", backref="employee")
    })

    mapper_registry.map_imperatively(Customer, customers_table, properties={
        "works": relationship("Work", backref="customer")
    })

    mapper_registry.map_imperatively(Work, works_table)


def create_tables():
    metadata.create_all(bind=engine)


def reset_id_sequence(session, table_name: str, pk_column: str):
    sequence_name = f"{table_name}_{pk_column}_seq"
    stmt = text(
        f"SELECT setval('{sequence_name}', COALESCE((SELECT MAX({pk_column}) FROM {table_name}) + 1, 1), false)"
    )
    session.execute(stmt)
    session.commit()