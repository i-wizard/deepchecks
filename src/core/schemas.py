from datetime import datetime
from typing import Optional, Union, Any
from pydantic import BaseModel, model_validator


class DBBaseModel(BaseModel):
    id: str
    created_at: datetime = None
    updated_at: Optional[datetime] = None

    @model_validator(mode='before')
    @classmethod
    def stringify_id(cls, data):
        if data.get("_id"):
            data["id"] = str(data["_id"])
        return data


class Interaction(DBBaseModel):
    identifier: int
    input: str
    output: str


class MetricResult(DBBaseModel):
    interaction_id: str
    metric_name: str
    input_value: float
    output_value: float


class Alerts(DBBaseModel):
    interaction_id: str
    metric_name: str
    alert_type: str
    element: str
    value: float
