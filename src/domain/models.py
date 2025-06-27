import datetime
from dataclasses import dataclass, field


@dataclass
class BaseModel:
    created_at: datetime.datetime
    updated_at: datetime.datetime


@dataclass
class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str

    employees: list = field(default_factory=list)
    customers: list = field(default_factory=list)


@dataclass
class BankAccount(BaseModel):
    iban: str
    bank_name: str
    bic: str

    employees: list = field(default_factory=list)


@dataclass
class Employee(BaseModel):
    name: str
    code: str
    hourly_rate: float
    company_name: str
    metadata: dict
    address_id: int
    bank_account_id: int

    works: list = field(default_factory=list)


@dataclass
class Customer(BaseModel):
    name: str
    metadata: dict
    invoice_name: str
    hourly_rate: float
    note: str
    address_id: int

    works: list = field(default_factory=list)


@dataclass
class Work:
    customer_id: int
    employee_id: int
    hours: float
    date: datetime.date
