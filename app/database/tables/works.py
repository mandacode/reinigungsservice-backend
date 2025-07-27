from sqlalchemy import Column, Integer, Table, ForeignKey, DateTime, func, Float, Date

from app.database.tables import metadata


works = Table(
    "works",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", ForeignKey("customers.id"), nullable=False),
    Column("employee_id", ForeignKey("employees.id"), nullable=False),
    Column("hours", Float, nullable=False),
    Column("date", Date, index=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)
