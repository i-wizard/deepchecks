from dataclasses import dataclass

from app.entities import BaseEntity


@dataclass
class MetricEntity(BaseEntity):
    interaction_id: str
    metric_name: str
    input_value: float
    output_value: float

    @classmethod
    def get_collection(cls):
        return "metric"

    def to_dict(self):
        return {
            "interaction_id": self.interaction_id,
            "metric_name": self.metric_name,
            "input_value": self.input_value,
            "output_value": self.output_value
        }
