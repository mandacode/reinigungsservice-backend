from typing import Generic, TypeVar

from domain.models import (
    Employee, Customer,  Address, BankAccount, Work, BaseModel
)


Model = TypeVar('Model', bound=BaseModel)

class BaseRepository(Generic[Model]):
    _model: Model

    def __init__(self, session):
        self._session = session

    def get_all(self) -> list[Model]:
        return self._session.query(self._model).all()

    def add_all(self, entities: list[Model]) -> None:
        self._session.add_all(entities)
        self._session.commit()

    def delete_all(self) -> None:
        self._session.query(self._model).delete()
        self._session.commit()


class EmployeeRepository(BaseRepository):
    _model = Employee


class CustomerRepository(BaseRepository):
    _model = Customer


class AddressRepository(BaseRepository):
    _model = Address


class BankAccountRepository(BaseRepository):
    _model = BankAccount


class WorkRepository(BaseRepository):
    _model = Work
