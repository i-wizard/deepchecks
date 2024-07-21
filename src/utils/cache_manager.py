from typing import Any, Union
import json

from src.config.redis_client import redis_client


class CacheManager:
    def __init__(self, client=None):
        if not client:
            client = redis_client
        self.client = client

    def set_key(self, key: str, data: Any, timeout: int = None):
        self.client.set(key, json.dumps(data), ex=timeout)

    def retrieve_key(self, key: str) -> Any:
        data: Union[bytes, None] = self.client.get(key)
        if data:
            data = json.loads(data)
        return data
    
    def delete_key(self, key: str):
        self.client.delete(key)
