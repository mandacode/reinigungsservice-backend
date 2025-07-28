import datetime

from pydantic import BaseModel, Field


class WorkCreateDTO(BaseModel):
    customer_id: int
    hours: float = Field(..., ge=0.5)


class WorkDayCreateDTO(BaseModel):
    employee_id: int
    works: list[WorkCreateDTO]


class WorksCreateRequestDTO(BaseModel):
    date: datetime.date
    work_days: list[WorkDayCreateDTO]
