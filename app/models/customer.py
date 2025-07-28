from dataclasses import dataclass, field

from app.models.address import Address
from app.models.base_model import BaseModel


@dataclass
class Customer(BaseModel):
    name: str
    metadata: dict
    invoice_name: str
    hourly_rate: float
    note: str
    address_id: int = None

    works: list = field(default_factory=list, repr=False)
    address: Address = field(default=None, repr=False)
