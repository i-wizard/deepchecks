from abc import ABC
from datetime import datetime, timezone
from typing import List, Union

from pymongo import cursor, DESCENDING
from pymongo.results import InsertOneResult

from app.entities import BaseEntity
from app.repositories import BaseRepository


class MongoDB(BaseRepository, ABC):
    def __init__(self, db: str) -> None:
        self.db = db

    def add(self, entity: BaseEntity) -> Union[InsertOneResult, None]:
        collection_name = entity.get_collection()
        collection = self.db[collection_name]
        document = entity.to_dict()
        now = datetime.now(timezone.utc)
        document["created_at"] = now
        document["updated_at"] = now
        return collection.insert_one(document)

    def add_many(self, entites: List[BaseEntity]):
        for entity in entites:
            self.add(entity)

    def get(self, collection: str,  filter=None, *args, **kwargs):
        if filter is None:
            filter = {}
        return self.db[collection].find_one(filter, *args, **kwargs)

    def insert_one(*args, **kwargs):
        ...

    def insert_many(*args, **kwargs):
        ...

    def list(self, collection: str, filter=None, *args, **kwargs) -> cursor.Cursor:
        if filter is None:
            filter = {}
        return self.db[collection].find(filter, *args, **kwargs).sort("created_at", DESCENDING)

    def find(self, filter=None, *args, **kwargs) -> cursor.Cursor:
        ...

    def find_one(self, filter=None, *args, **kwargs):
        ...

    def set_collection(self, filter=None, *args, **kwargs):
        ...

    def delete_one(self, filter, *args, **kwargs):
        return self.collection.delete_one(filter, *args, **kwargs)

    def commit(self) -> None:
        ...
