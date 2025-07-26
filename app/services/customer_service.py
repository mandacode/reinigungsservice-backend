from app.repositories.customer_repository import CustomerRepository
from app.models.customer import Customer


class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository

    async def get_all_customers(self) -> list[Customer]:
        return await self._customer_repository.get_all()
