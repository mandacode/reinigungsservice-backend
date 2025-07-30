import datetime
from dataclasses import dataclass

from app.models.base_model import BaseModel


@dataclass
class RefreshToken(BaseModel):
    token: str
    expires_at: datetime.datetime
    user_id: int
