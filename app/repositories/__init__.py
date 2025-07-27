from app.repositories.base_repository import BaseRepository
from app.models.address import Address
from app.models.bank_account import BankAccount


class AddressRepository(BaseRepository):
    _model = Address


class BankAccountRepository(BaseRepository):
    _model = BankAccount
