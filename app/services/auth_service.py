import datetime

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.models.user import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenIsBlacklistedError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
    ):
        self._user_repository = user_repository
        self._refresh_token_repository = refresh_token_repository

    async def authenticate(self, username: str, password: str) -> User | None:
        user = await self._user_repository.get_by_username(username)

        if not user or not self.verify_password(password, user.password):
            return None

        return user

    async def get_current_user(self, token: str) -> User:
        payload = jwt.decode(
            token, key=settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id = payload.get("sub")
        return await self._user_repository.get(int(user_id))

    async def delete_refresh_token(self, token: str):
        await self._refresh_token_repository.delete_by_token(token)

    async def verify_refresh_token(self, token: str) -> bool:
        is_revoked = await self._refresh_token_repository.is_revoked(token)
        print(f"Token {token} is revoked: {is_revoked}")
        if is_revoked:
            return False

        try:
            payload = jwt.decode(
                token, key=settings.secret_key, algorithms=[settings.algorithm]
            )
            print(f"Decoded payload: {payload}")
            user_id = payload.get("sub")
            if not user_id:
                return False

        except JWTError:
            print(f"JWTError: Invalid token {token}")
            await self._refresh_token_repository.delete_by_token(token)
            return False
        return True

    def create_access_token(self, data: dict):
        return self._create_token(data, settings.access_token_lifespan)

    async def create_refresh_token(self, data: dict) -> str:
        refresh_token = self._create_token(
            data=data,
            lifespan=settings.refresh_token_lifespan
        )
        await self._refresh_token_repository.add(
            RefreshToken(
                token=refresh_token,
                user_id=int(data["sub"]),
                # TODO set the correct expiration time
                expires_at=(
                        datetime.datetime.now(datetime.UTC) +
                        datetime.timedelta(minutes=settings.refresh_token_lifespan)
                ),
            )
        )
        return refresh_token

    @staticmethod
    def _create_token(data: dict, lifespan: int) -> str:
        expires_in = datetime.timedelta(seconds=lifespan)

        to_encode = data.copy()
        now = datetime.datetime.now(datetime.UTC)

        expire = now + expires_in

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            key=settings.secret_key,
            algorithm=settings.algorithm
        )

        return encoded_jwt

    async def register_user(self, username: str, password: str):
        user = await self._user_repository.get_by_username(username)
        if user:
            raise UserAlreadyExistsError
        user = User(username=username, password=self.get_password_hash(password))
        await self._user_repository.add(user)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)


# TODO
"""
User logs in with username and password and he receives an access token (body) and a refresh token (cookie)
User can use the access token to access protected routes, and the refresh token to get a new access token when it expires.

When the user logs out, the access token is blacklisted and the refresh token is deleted from the database.
When the user logs in again, a new access token and refresh token are created.


"""