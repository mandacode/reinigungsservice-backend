from sqlalchemy import select

from app.models.blacklisted_token import BlacklistedToken
from app.repositories.base_repository import BaseRepository


class BlacklistedTokenRepository(BaseRepository):
    _model = BlacklistedToken

    async def is_blacklisted(self, token: str) -> bool:
        stmt = select(self._model).where(self._model.token == token)
        result = await self._session.execute(stmt)
        return result.scalars().first() is not None
