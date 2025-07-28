from sqlalchemy import (
    Column,
    Integer,
    Table,
    String,
    DECIMAL,
    JSON,
    ForeignKey,
    DateTime,
    func,
)

from app.database.tables import metadata

employees = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False, index=True),
    Column("code", String(3), nullable=False, index=True),
    Column("hourly_rate", DECIMAL(4, 2), nullable=False, default=12.00),
    Column("company_name", String(100), nullable=True),
    Column("metadata", JSON, default=dict),
    Column("address_id", ForeignKey("addresses.id"), nullable=True),
    Column("bank_account_id", ForeignKey("bank_accounts.id"), nullable=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)
