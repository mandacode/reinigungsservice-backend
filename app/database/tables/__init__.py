from sqlalchemy import MetaData

metadata = MetaData()

from .users import users
from .customers import customers
from .addresses import addresses
from .bank_accounts import bank_accounts
from .blacklisted_tokens import blacklisted_tokens
from .employees import employees
from .works import works
