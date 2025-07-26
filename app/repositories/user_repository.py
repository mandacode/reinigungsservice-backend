from sqlalchemy import select

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    _model = User

    async def get_by_username(self, username: str) -> User:
        stmt = select(self._model).where(self._model.username == username)
        result = await self._session.execute(stmt)
        return result.scalars().first()
