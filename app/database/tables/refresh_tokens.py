from sqlalchemy import Column, Integer, Table, String, ForeignKey, DateTime, func

from app.database.tables import metadata

refresh_tokens = Table(
    "refresh_tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("token", String(500), nullable=False, unique=True),
    Column("expires_at", DateTime(timezone=True), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)
