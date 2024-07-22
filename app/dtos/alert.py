from app.dtos import BaseResponse


class AlertResponse(BaseResponse):
    interaction_id: str
    metric_name: str
    alert_type: str
    element: str
    value: float
