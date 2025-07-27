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

customers = Table(
    "customers",
    metadata,
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
