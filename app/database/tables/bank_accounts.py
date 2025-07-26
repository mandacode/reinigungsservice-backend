from sqlalchemy import Column, Integer, Table, String, DateTime, func

from app.database.tables import metadata


bank_accounts = Table(
    "bank_accounts", metadata,
    Column("id", Integer, primary_key=True),
    Column("iban", String(40), nullable=False),
    Column("bank_name", String(100), nullable=False),
    Column("bic", String(11), nullable=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)