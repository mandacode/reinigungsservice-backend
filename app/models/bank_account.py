from dataclasses import dataclass, field

from app.models.base_model import BaseModel


@dataclass
class BankAccount(BaseModel):
    iban: str
    bank_name: str
    bic: str

    employees: list = field(default_factory=list, repr=False)
