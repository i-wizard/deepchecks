from typing import List

from src.core.models import alert_collection


class AlertService:
    collection = alert_collection

    @classmethod
    def create_alerts(cls, data: List[dict]):
        alert_collection.insert_many(data)
        
    @classmethod
    def list_alerts(cls, query):
        return cls.collection.find(query)
