from dataclasses import field, dataclass

from app.models.base_model import BaseModel


@dataclass
class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str

    employees: list = field(default_factory=list, repr=False)
    customers: list = field(default_factory=list, repr=False)
