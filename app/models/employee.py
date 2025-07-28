from dataclasses import dataclass, field

from app.models.address import Address
from app.models.bank_account import BankAccount
from app.models.base_model import BaseModel


@dataclass
class Employee(BaseModel):
    name: str
    code: str
    hourly_rate: float
    company_name: str
    metadata: dict
    address_id: int = None
    bank_account_id: int = None

    works: list = field(default_factory=list, repr=False)
    address: Address = field(default=None, repr=False)
    bank_account: BankAccount = field(default=None, repr=False)
