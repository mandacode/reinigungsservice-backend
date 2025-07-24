import datetime

from jose import jwt
from passlib.context import CryptContext

from db.repositories import UserRepository, BlacklistedTokenRepository
from config import SECRET_KEY, ALGORITHM
from domain.models import User, BlacklistedToken


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenIsBlacklistedError(Exception):
    pass


class AuthService:

    def __init__(
            self,
            user_repository: UserRepository,
            blacklisted_token_repository: BlacklistedTokenRepository
    ):
        self._user_repository = user_repository
        self._blacklisted_token_repository = blacklisted_token_repository

    async def authenticate(self, username: str, password: str) -> User | None:
        user = await self._user_repository.get_by_username(username)

        if not user or not self.verify_password(password, user.password):
            return None

        return user

    async def get_current_user(self, token: str) -> User:

        if await self._blacklisted_token_repository.is_blacklisted(token):
            raise TokenIsBlacklistedError

        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        return await self._user_repository.get_by_username(username)

    async def blacklist_token(self, token: str, user_id: int):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires_at = payload.get("exp")

        if expires_at:
            exp = datetime.datetime.fromtimestamp(expires_at, tz=datetime.UTC)
            blacklisted_token = BlacklistedToken(
                token=token,
                expires_at=exp,
                user_id=user_id,

            )
            print(f"Blacklisting token: {blacklisted_token}")
            await self._blacklisted_token_repository.add(blacklisted_token)



    @staticmethod
    def create_access_token(data: dict, expires_delta):
        to_encode = data.copy()
        now = datetime.datetime.now(datetime.UTC)

        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + datetime.timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
