from sqlalchemy import select, delete

from app.models.refresh_token import RefreshToken
from app.repositories.base_repository import BaseRepository


class RefreshTokenRepository(BaseRepository):
    _model = RefreshToken

    async def is_revoked(self, token: str) -> bool:
        stmt = select(self._model).where(self._model.token == token)
        result = await self._session.execute(stmt)
        return result.scalars().first() is None

    async def delete_by_token(self, token: str) -> None:
        stmt = delete(self._model).where(self._model.token == token)
        await self._session.execute(stmt)
        await self._session.commit()
