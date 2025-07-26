from dataclasses import dataclass

from app.models.base_model import BaseModel


@dataclass
class User(BaseModel):
    username: str
    password: str
