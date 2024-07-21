from datetime import datetime, timezone
from typing import List

from pymongo import MongoClient, cursor, DESCENDING
from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult

from src.config.settings import settings


uri = settings.MONGO_URI or settings.DATABASE_URL
client = MongoClient(uri)
db = client["deepchecks_db"]

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(e)


class MongoBase:
    def __init__(self, collection_name: str):
        self.collection = db[collection_name]

    def find(self, filter=None, *args, **kwargs) -> cursor.Cursor:
        if filter is None:
            filter = {}
        return self.collection.find(filter, *args, **kwargs).sort("created_at", DESCENDING)

    def find_one(self, filter=None, *args, **kwargs):
        if filter is None:
            filter = {}
        return self.collection.find_one(filter, *args, **kwargs)

    def insert_one(self, document: dict) -> InsertOneResult:
        now = datetime.now(timezone.utc)
        document["created_at"] = now
        document["updated_at"] = now
        return self.collection.insert_one(document)

    def insert_many(self, document: List[dict]) -> None:
        now = datetime.now(timezone.utc)
        for obj in document:
            obj["created_at"] = now
            obj["updated_at"] = now
            self.collection.insert_one(obj)

    def update_one(self, filter: dict, update_data: dict, *args, **kwargs) -> UpdateResult:
        update_data["$set"]["updated_at"] = datetime.now(timezone.utc)
        return self.collection.update_one(filter, update_data, *args, **kwargs)

    def update_many(self, filter: dict, update_data: dict, *args, **kwargs) -> UpdateResult:
        update_data["$set"]["updated_at"] = datetime.now(timezone.utc)
        return self.collection.update_many(filter, update_data, *args, **kwargs)

    def delete_one(self, filter, *args, **kwargs):
        return self.collection.delete_one(filter, *args, **kwargs)

    def count_documents(self, query: dict) -> int:
        return self.collection.count_documents(query)
