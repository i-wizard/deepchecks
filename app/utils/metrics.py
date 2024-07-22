from typing import List, Dict

from app.config.redis_client import redis_client
from app.config.settings import settings
from app.repositories.memory import MemoryRepository
from app.utils.key_builder import KeyBuilder
from app.utils.helper import has_outlier

# New metrics can be added by simply inheriting from this Metric base class


class Metric:
    def __init__(self, name):
        self.name = name

    def calculate(self, text: str) -> float:
        raise NotImplementedError

    def alert_checker(self, metric_data: dict) -> List[Dict[str, str]]:
        raise NotImplementedError


class LengthMetric(Metric):
    def __init__(self):
        super().__init__("length")

    def calculate(self, text: str) -> float:
        words = text.split(" ")
        return len(words)

    def alert_checker(self, metric_data: dict) -> List[Dict[str, str]]:
        def create_alert(element: str, value: str, alert_type: str):
            return {"interaction_id": metric_data["interaction_id"],
                    "metric_name": metric_data["metric_name"],
                    "element": element,
                    "value": value,
                    "alert_type": alert_type}

        alerts: List[Dict[str, str]] = []
        length_metric_threshold = settings.LENGTH_METRIC_THRESHOLD
        minimum_value = length_metric_threshold["minimum"]
        maximum_value = length_metric_threshold["maximum"]
        if metric_data.get("input_value") < minimum_value:
            alerts.append(create_alert(
                "input", metric_data['input_value'], 'length_lesser_than_threshold'))
        if metric_data.get('input_value') > maximum_value:
            alerts.append(create_alert(
                "input", metric_data['input_value'], 'length_greater_than_threshold'))
        if metric_data.get("output_value") < minimum_value:
            alerts.append(create_alert(
                "output", metric_data['output_value'], 'length_lesser_than_threshold'))
        if metric_data.get('output_value') > maximum_value:
            alerts.append(create_alert(
                "output", metric_data['output_value'], 'length_greater_than_threshold'))
        cache = MemoryRepository(redis_client)
        saved_input_lengths = cache.get(
            KeyBuilder.interaction_input_length()) or []
        saved_output_lengths = cache.get(
            KeyBuilder.interaction_output_length()) or []
        if has_outlier(metric_data["input_value"], saved_input_lengths):
            alerts.append(create_alert(
                "input", metric_data['input_value'], "length_is_outlier"))
        if has_outlier(metric_data["output_value"], saved_output_lengths):
            alerts.append(create_alert(
                "input", metric_data['output_value'], "length_is_outlier"))
        return alerts
