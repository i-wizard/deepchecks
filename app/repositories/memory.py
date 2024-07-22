from abc import ABC
from typing import Iterable
from typing import Optional, Any, Union
import json

from app.entities import BaseEntity
from app.repositories import BaseRepository


class MemoryRepository(BaseRepository, ABC):
    def __init__(self, db) -> None:
        self.client = db
        self.data: list[BaseEntity] = []

    def add(self, key: str, data: Any, timeout: int = None):
        self.client.set(key, json.dumps(data), ex=timeout)

    def get(self, key: str) -> Optional[BaseEntity]:
        data: Union[bytes, None] = self.client.get(key)
        if data:
            data = json.loads(data)
        return data

    def remove(self, key: str):
        self.client.delete(key)

    def list(self) -> Iterable[BaseEntity]:
        ...

    def commit(self) -> None:
        ...

    def insert_one(*args, **kwargs):
        ...

    def insert_many(*args, **kwargs):
        ...

    def set_collection(self, filter=None, *args, **kwargs):
        ...

    def delete_one(self, id: str) -> bool:
        ...

    def find(self) -> Iterable[BaseEntity]:
        ...

    def find_one(self) -> Iterable[BaseEntity]:
        ...

    def add_many(self, id: str) -> Optional[BaseEntity]:
        ...
