from typing import Any, Dict, List

from app.dtos.alert import AlertResponse
from app.entities.alert import AlertEntity
from app.repositories import BaseRepository


class AlertUseCase:
    def __init__(self, repo: BaseRepository):
        self.repo = repo

    async def execute(self, data: Dict[str, List[Dict[str, Any]]]):
        alerts = data['alerts']
        alert_entities = [AlertEntity(**alert) for alert in alerts]
        self.repo.add_many(alert_entities)


class ListAlertUseCase:
    def __init__(self, repo: BaseRepository):
        self.repo = repo

    def execute(self, query: Dict[str, Any]):
        alerts = self.repo.list(AlertEntity.get_collection(), query)
        # Paginate this response to improve endpoint response time
        return [AlertResponse(**alert) for alert in alerts]
