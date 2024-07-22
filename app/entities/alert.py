from dataclasses import dataclass

from app.entities import BaseEntity


@dataclass
class AlertEntity(BaseEntity):
    interaction_id: str
    metric_name: str
    alert_type: str
    element: str
    value: float

    @classmethod
    def get_collection(cls):
        return "alert"

    def to_dict(self):
        return {
            "interaction_id": self.interaction_id,
            "metric_name": self.metric_name,
            "alert_type": self.alert_type,
            "element": self.element,
            "value": self.value
        }
