from typing import List, Union

from src.core.schemas import MetricResult, Alerts, Interaction


def list_metric_serializer(metrics) -> List[dict]:
    return [metric_serializer(data) for data in metrics]


def metric_serializer(metric, exclude: Union[dict, None] = None) -> dict:
    """
    A helper function for parsing a Mongo db object to
    a Python dict
    """
    if not exclude:
        exclude = {}
    return MetricResult(**metric).model_dump(mode='json', exclude=exclude)


def list_alerts_serializer(alerts) -> List[dict]:
    return [alert_serializer(data) for data in alerts]


def alert_serializer(alert, exclude: Union[dict, None] = None) -> dict:
    if not exclude:
        exclude = {}
    return Alerts(**alert).model_dump(mode='json', exclude=exclude)


def list_interaction_serializer(interactions) -> List[dict]:
    return [interaction_serializer(data) for data in interactions]


def interaction_serializer(interaction, exclude: Union[dict, None] = None) -> dict:
    if not exclude:
        exclude = {}
    return Interaction(**interaction).model_dump(mode='json', exclude=exclude)
