from app.models.address import Address
from app.repositories.customer_repository import CustomerRepository
from app.repositories import AddressRepository
from app.models.customer import Customer
from app.schemas.customers import CustomerCreateDTO


class CustomerService:
    def __init__(
            self,
            customer_repository: CustomerRepository,
            address_repository: AddressRepository
    ):
        self._customer_repository = customer_repository
        self._address_repository = address_repository

    async def get_all_customers(self) -> list[Customer]:
        return await self._customer_repository.get_all()

    async def create_customer(self, data: CustomerCreateDTO) -> Customer:
        address = Address(
            street_address=data.address.street_address,
            city=data.address.city,
            postal_code=data.address.postal_code,
        )
        await self._address_repository.add(address)
        customer = Customer(
            name=data.name,
            invoice_name=data.invoice_name,
            note=data.note,
            metadata=data.metadata,
            hourly_rate=data.hourly_rate,
        )
        customer.address = address
        return await self._customer_repository.add(customer)
