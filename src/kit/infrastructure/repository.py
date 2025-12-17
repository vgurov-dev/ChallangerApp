from abc import ABC, abstractmethod
from typing import Iterable


class Repository[T](ABC):
    """
    Abstract base class for repositories.
    """
    @abstractmethod
    def get_by_id(
            self,
            id: str | int
    ):
        raise NotImplementedError

    @abstractmethod
    def update_by_id(self, id: str | int) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_one(self,
                row: T):
        raise NotImplementedError

    @abstractmethod
    def add_many(
            self,
            rows: Iterable[T]
    ):
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, id):
        raise NotImplementedError



