from dataclasses import dataclass
from math import ceil
from typing import Union, Callable, List
import json

from fastapi import Response
from pymongo.collection import Collection
from pymongo.cursor import Cursor


@dataclass
class ResponseModel:
    data: Union[dict, list]
    serializer: Callable = None
    status_code: int = 200
    message: str = "Request Successful"
    context = {}
    serialized_data = None

    def send(self):
        response_data = {
            **self.context,
            "data": self.serialized_data or (self.serializer(self.data) if self.serializer else self.data),
            "message": self.message
        }
        encoded_data = json.dumps(
            response_data,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(", ", ":")).encode("utf-8")
        if self.status_code == 204:  # Since this means no content we return an empty response data
            encoded_data = ""
        return Response(
            content=encoded_data,
            headers={"Content-Type": "application/json"},
            status_code=self.status_code
        )

    def paginate_response(self, page_number: int = 1, limit: int = 10, query: Union[dict, None] = None, collection: Union[Collection, None] = None):
        paginated_data_context = paginator(
            self.data, page_number, limit, self.serializer, query, collection)
        self.serialized_data = paginated_data_context.pop("data")
        self.context = paginated_data_context
        return self.send()


def paginator(collection_data: list, page_number: int, limit: int, serializer: Callable, query: dict, collection: Collection) -> dict:
    total_count: int = collection.count_documents(query)
    paginated_collection_data: Cursor = collection_data.skip(
        (page_number - 1) * limit).limit(limit)
    paginated_data: List[dict] = serializer(paginated_collection_data)
    count: int = len(paginated_data)
    current_page: int = page_number
    total_pages: int = ceil(total_count/limit)
    return {
        "data": paginated_data,
        "current_result": count,
        "total_result": total_count,
        "current_page_number": current_page,
        "total_page_number": total_pages
    }
