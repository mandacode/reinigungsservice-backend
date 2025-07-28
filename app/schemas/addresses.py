from pydantic import BaseModel


class AddressCreateDTO(BaseModel):
    street_address: str
    postal_code: str
    city: str
