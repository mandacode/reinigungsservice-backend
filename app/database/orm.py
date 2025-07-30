from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import registry, relationship

from app.database.tables import metadata
from app.database.tables.addresses import addresses
from app.database.tables.bank_accounts import bank_accounts
from app.database.tables.customers import customers
from app.database.tables.employees import employees
from app.database.tables.users import users
from app.database.tables.works import works
from app.database.tables.refresh_tokens import refresh_tokens
from app.models.address import Address
from app.models.bank_account import BankAccount
from app.models.employee import Employee
from app.models.customer import Customer
from app.models.work import Work
from app.models.user import User
from app.models.refresh_token import RefreshToken

mapper_registry = registry()


def run_mappers():
    mapper_registry.map_imperatively(Address, addresses)
    mapper_registry.map_imperatively(BankAccount, bank_accounts)

    mapper_registry.map_imperatively(
        Employee,
        employees,
        properties={
            "works": relationship(Work, backref="employee"),
            "address": relationship(Address, backref="employees", uselist=False),
            "bank_account": relationship(
                BankAccount, backref="employees", uselist=False
            ),
        },
    )

    mapper_registry.map_imperatively(
        Customer,
        customers,
        properties={
            "works": relationship("Work", backref="customer"),
            "address": relationship(Address, backref="customers", uselist=False),
        },
    )

    mapper_registry.map_imperatively(Work, works)

    mapper_registry.map_imperatively(User, users)
    mapper_registry.map_imperatively(RefreshToken, refresh_tokens)


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def reset_id_sequence(session: AsyncSession, table_name: str, pk_column: str):
    sequence_name = f"{table_name}_{pk_column}_seq"
    stmt = text(
        f"SELECT setval('{sequence_name}', COALESCE((SELECT MAX({pk_column}) FROM {table_name}) + 1, 1), false)"
    )
    await session.execute(stmt)
    await session.commit()
