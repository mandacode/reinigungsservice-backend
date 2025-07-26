import datetime

from pydantic import BaseModel


class InvoicesCreateDTO(BaseModel):
    start_date: datetime.date
    end_date: datetime.date
    last_invoice_number: int
