from db.repositories import CustomerRepository
from domain.models import Customer


class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository

    def get_all_customers(self) -> list[Customer]:
        return self._customer_repository.get_all()
