from abc import ABC, abstractmethod
from typing import Iterable, TypeVar, Optional, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from kit.exceptions.repository import RepositoryItemNotFound
from backend.app.repository.challenge import ChallengeSQLAlchemyRepository


T = TypeVar('T')

class Repository[T](ABC):
    """
    Abstract base class for repositories.
    """
    @abstractmethod
    def get_by_id(
            self,
            id: str | int
    ) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_one(self,
                row: T):
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, id):
        raise NotImplementedError


class SQLAlchemyRepository[T](Repository[T]):
    """
    Abstract base class for SQLAlchemy repositories.
    """
    _session: AsyncSession

    def __init__(
            self,
            session: AsyncSession,
            model: type[T]
    ):
        super().__init__(session)
        self._model = model

    async def get_by_id(
            self,
            id: str | int
    ) -> Optional[Any]:
        stmt = select(self._model).where(self._model.id == id)
        result = await self._session.execute(stmt).scalar()
        if result is None:
            raise RepositoryItemNotFound
        return result

    async def get_all(self, **kwargs):
        stmt = select(self._model)
        result = await self._session.execute(stmt, **kwargs)
        return result.all()


    async def add_one(self,
                row: type[T]):
        self.session.add(row)
        await self._session.commit()

    async def delete_one(self, row: type[T]) -> bool:
        row.is_disabled = True
        self._session.add(row)
        await  self._session.commit()
        return True


