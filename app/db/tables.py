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
    func, text, Float
)
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import registry, relationship

from app.domain.models import (
    Employee, Customer, Work, Address, BankAccount, User, BlacklistedToken
)

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
    Column("hours", Float, nullable=False),
    Column("date", Date, index=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)

users_table = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), nullable=False, unique=True),
    Column("password", String(100), nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)

blacklisted_tokens_table = Table(
    "blacklisted_tokens", metadata,
    Column("id", Integer, primary_key=True),
    Column("token", String(500), nullable=False, unique=True),
    Column("expires_at", DateTime, nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)

def run_mappers():
    mapper_registry.map_imperatively(Address, addresses_table)
    mapper_registry.map_imperatively(BankAccount, bank_accounts_table)

    mapper_registry.map_imperatively(Employee, employees_table, properties={
        "works": relationship(Work, backref="employee"),
        "address": relationship(Address, backref="employees", uselist=False),
        "bank_account": relationship(BankAccount, backref="employees", uselist=False)
    })

    mapper_registry.map_imperatively(Customer, customers_table, properties={
        "works": relationship("Work", backref="customer"),
        "address": relationship(Address, backref="customers", uselist=False)
    })

    mapper_registry.map_imperatively(Work, works_table)

    mapper_registry.map_imperatively(User, users_table)
    mapper_registry.map_imperatively(BlacklistedToken, blacklisted_tokens_table)


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def reset_id_sequence(session, table_name: str, pk_column: str):
    sequence_name = f"{table_name}_{pk_column}_seq"
    stmt = text(
        f"SELECT setval('{sequence_name}', COALESCE((SELECT MAX({pk_column}) FROM {table_name}) + 1, 1), false)"
    )
    await session.execute(stmt)
    await session.commit()