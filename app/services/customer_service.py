from app.db.repositories import CustomerRepository
from app.domain.models import Customer


class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository

    async def get_all_customers(self) -> list[Customer]:
        return await self._customer_repository.get_all()
