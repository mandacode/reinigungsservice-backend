import datetime
from dataclasses import dataclass


@dataclass
class Work:
    customer_id: int
    employee_id: int
    hours: float
    date: datetime.date
