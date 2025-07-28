from pydantic import BaseModel, Field

from app.schemas.addresses import AddressCreateDTO


class CustomerCreateDTO(BaseModel):
    name: str
    invoice_name: str = None
    hourly_rate: float = Field(..., ge=0.0)
    note: str
    metadata: dict = {}
    address: AddressCreateDTO


class CustomerDTO(BaseModel):
    id: int
    name: str
    invoice_name: str = None
