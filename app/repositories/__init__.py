from abc import ABC
from abc import abstractmethod
from typing import Iterable
from typing import Optional

from app.entities import BaseEntity


class ContextManagerRepository(ABC):
    @abstractmethod
    def set_collection(self):
        ...

    @abstractmethod
    def commit(self):
        ...

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.commit()


class BaseReadOnlyRepository(ABC):
    @abstractmethod
    def get(self, id: str) -> Optional[BaseEntity]:
        ...

    @abstractmethod
    def list(self) -> Iterable[BaseEntity]:
        ...

    @abstractmethod
    def find_one(self) -> Iterable[BaseEntity]:
        ...

    @abstractmethod
    def find(self) -> Iterable[BaseEntity]:
        ...

    @abstractmethod
    def set_collection(self, filter=None, *args, **kwargs):
        ...


class BaseWriteOnlyRepository(ContextManagerRepository):
    @abstractmethod
    def delete_one(self, id: str) -> bool:
        ...

    @abstractmethod
    def add(self, id: str) -> Optional[BaseEntity]:
        ...

    @abstractmethod
    def add_many(self, id: str) -> Optional[BaseEntity]:
        ...

    @abstractmethod
    def insert_one(self, id: str) -> Optional[BaseEntity]:
        ...

    @abstractmethod
    def insert_many(self, id: str) -> Optional[BaseEntity]:
        ...


class BaseRepository(BaseReadOnlyRepository, BaseWriteOnlyRepository, ABC):
    ...
