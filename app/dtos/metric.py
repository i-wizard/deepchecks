from app.dtos import BaseResponse


class MetricResponse(BaseResponse):
    interaction_id: str
    metric_name: str
    input_value: float
    output_value: float
