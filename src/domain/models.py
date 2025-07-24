import datetime
from dataclasses import dataclass, field


@dataclass
class BaseModel:
    pass


@dataclass
class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str

    employees: list = field(default_factory=list, repr=False)
    customers: list = field(default_factory=list, repr=False)


@dataclass
class BankAccount(BaseModel):
    iban: str
    bank_name: str
    bic: str

    employees: list = field(default_factory=list, repr=False)


@dataclass
class Employee(BaseModel):
    name: str
    code: str
    hourly_rate: float
    company_name: str
    metadata: dict
    address_id: int
    bank_account_id: int

    works: list = field(default_factory=list, repr=False)
    address: Address = field(default=None, repr=False)
    bank_account: BankAccount = field(default=None, repr=False)


@dataclass
class Customer(BaseModel):
    name: str
    metadata: dict
    invoice_name: str
    hourly_rate: float
    note: str
    address_id: int

    works: list = field(default_factory=list, repr=False)
    address: Address = field(default=None, repr=False)


@dataclass
class Work:
    customer_id: int
    employee_id: int
    hours: float
    date: datetime.date

# TODO move to separate package 'auth'

@dataclass
class User(BaseModel):
    username: str
    password: str


@dataclass
class BlacklistedToken(BaseModel):
    token: str
    expires_at: datetime.datetime
    user_id: int
