from pydantic import BaseModel, Field

from app.schemas.addresses import AddressCreateDTO


class BankAccountCreateDTO(BaseModel):
    iban: str
    bic: str
    bank_name: str


class EmployeeCreateDTO(BaseModel):
    name: str
    code: str = Field(..., max_length=3)
    hourly_rate: float = Field(..., ge=0.0)
    company_name: str
    metadata: dict = {}
    address: AddressCreateDTO
    bank_account: BankAccountCreateDTO


class EmployeeDTO(BaseModel):
    id: int
    name: str
    code: str = Field(..., max_length=3)
