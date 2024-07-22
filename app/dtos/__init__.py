from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class BaseResponse(BaseModel):
    id: str
    created_at: datetime = None
    updated_at: Optional[datetime] = None

    @model_validator(mode='before')
    @classmethod
    def stringify_id(cls, data):
        if data.get("_id"):
            data["id"] = str(data["_id"])
        return data

    def send(self, exclude):
        if not exclude:
            exclude = {}
        self.model_dump(mode='json', exclude=exclude)
