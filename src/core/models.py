# module specific database models
from src.config.db import MongoBase


class InteractionCollection(MongoBase):
    def __init__(self):
        super().__init__("interaction")


interaction_collection = InteractionCollection()


class MetricCollection(MongoBase):
    def __init__(self):
        super().__init__("metric")


metric_collection = MetricCollection()


class AlertCollection(MongoBase):
    def __init__(self):
        super().__init__("alert")


alert_collection = AlertCollection()
