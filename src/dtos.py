import datetime

from pydantic import BaseModel, Field


class EmployeeDTO(BaseModel):
    id: int
    name: str
    code: str = Field(..., max_length=2)


class CustomerDTO(BaseModel):
    id: int
    name: str
    invoice_name: str = None


class WorkCreateDTO(BaseModel):
    customer_id: int
    hours: float = Field(..., ge=0.5)


class WorkDayCreateDTO(BaseModel):
    employee_id: int
    works: list[WorkCreateDTO]


class WorksCreateRequestDTO(BaseModel):
    date: datetime.date
    work_days: list[WorkDayCreateDTO]


class InvoicesCreateDTO(BaseModel):
    start_date: datetime.date
    end_date: datetime.date
    last_invoice_number: int
