from typing import Dict, Any

from app.config.redis_client import redis_client
from app.dtos.metric import MetricResponse
from app.entities.metric import MetricEntity
from app.repositories import BaseRepository
from app.repositories.memory import MemoryRepository
from app.utils.key_builder import KeyBuilder


class CreateMetricUseCase:
    def __init__(self, repo: BaseRepository):
        self.repo = repo
        self.repo.set_collection('metrics')

    async def execute(self, data: Dict[str, Any]):
        metric_entity = MetricEntity(**data)
        result = self.repo.add(metric_entity)
        memory_repo = MemoryRepository(redis_client)
        await CacheMetricUseCase(memory_repo).execute(data)

        return result.inserted_id


class ListMetricsUseCase:
    def __init__(self, repo: BaseRepository):
        self.repo = repo

    def execute(self, query: Dict[str, Any]):
        metrics = self.repo.list(MetricEntity.get_collection(), query)
        # Paginate this response to improve endpoint response time
        return [MetricResponse(**metric) for metric in metrics]


class CacheMetricUseCase:
    def __init__(self, repo: BaseRepository):
        self.repo = repo

    async def execute(self, data: Dict[str, Any]):

        input_length_key = KeyBuilder.interaction_input_length()
        output_length_key = KeyBuilder.interaction_output_length()

        saved_input_lengths = self.repo.get(input_length_key) or []
        saved_output_lengths = self.repo.get(output_length_key) or []

        saved_input_lengths.append(data['input_value'])
        self.repo.add(input_length_key, saved_input_lengths)

        saved_output_lengths.append(data['output_value'])
        self.repo.add(output_length_key, saved_output_lengths)
