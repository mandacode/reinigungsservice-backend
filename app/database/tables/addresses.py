from sqlalchemy import Column, Integer, Table, String, DateTime, func

from app.database.tables import metadata


addresses = Table(
    "addresses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("street_address", String(100), nullable=False),
    Column("postal_code", String(6), nullable=False),
    Column("city", String(50), nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)
