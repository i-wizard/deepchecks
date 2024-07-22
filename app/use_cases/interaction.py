from typing import Iterable, Dict, List
import traceback


from app.dtos.interaction import InteractionResponse
from app.entities import BaseEntity
from app.entities.interaction import InteractionEntity
from app.repositories import BaseRepository
from app.utils.logger import CustomLogger
from app.utils.metrics import LengthMetric
from app.use_cases import BaseUseCase
from app.use_cases.metric import CreateMetricUseCase
from app.use_cases.alert import AlertUseCase
from app.entities.interaction import InteractionEntity


class InteractionListUseCase(BaseUseCase):
    repo: BaseRepository

    def __init__(self, repo: BaseRepository) -> None:
        self.repo = repo

    def execute(self) -> Iterable[BaseEntity]:
        interactions = self.repo.list(InteractionEntity.get_collection(), {})
        # Paginate this response to improve endpoint response time
        return [InteractionResponse(**interaction) for interaction in interactions]


class SaveInteractionsUseCase(BaseUseCase):
    def __init__(self, repo: BaseRepository):
        self.repo = repo
        self.length_metric = LengthMetric()
        self.metric_use_case = CreateMetricUseCase(repo)
        self.alert_user_case = AlertUseCase(repo)

    async def execute(self, interactions: List[Dict[str, str]]):
        for interaction in interactions:
            try:
                interaction_entity = InteractionEntity(**interaction)
                result = self.repo.add(interaction_entity)
                interaction_id = result.inserted_id

                input_length = self.length_metric.calculate(
                    interaction["input"])
                output_length = self.length_metric.calculate(
                    interaction["output"])
                metric_result = {
                    "interaction_id": str(interaction_id),
                    "metric_name": self.length_metric.name,
                    "input_value": input_length,
                    "output_value": output_length
                }
                await self.metric_use_case.execute(metric_result)
                alerts = self.length_metric.alert_checker(metric_result)
                if alerts:
                    await self.alert_user_case.execute({"alerts": alerts})
            except Exception as e:
                extra = {"traceback": traceback.format_exc(), "error": str(e)}
                CustomLogger.error(
                    "Error saving interaction to DB", extra=extra)
