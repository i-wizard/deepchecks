from typing import List, Dict
import os
import traceback

import pandas as pd

from src.core.models import interaction_collection
from src.core.services.metric import MetricService
from src.core.services.alert import AlertService
from src.core.utils.metrics import LengthMetric
from src.utils.logger import CustomLogger


class InteractionService:
    collection = interaction_collection

    @classmethod
    async def process_csv(cls, file_path: str):
        # we read the data in chunks to handle large files efficiently
        try:
            # we should run some sort of preprocessing to handle bad rows
            reader = pd.read_csv(
                file_path, skipinitialspace=True, chunksize=10, on_bad_lines='skip')
            # we read the data in chunks to handle large files efficiently
            for chunk in reader:
                interactions = []
                for _, row in chunk.iterrows():
                    interaction = {"identifier": row.get("id"), "input": row.get(
                        "Input"), "output": row.get("Output")}
                    interactions.append(interaction)
                await cls.save_interactions_to_db(interactions)

        except Exception as e:
            extra = {"traceback": traceback.format_exc(), "error": str(e)}
            CustomLogger.error(
                "Error occured processing LLM interaction CSV file", extra=extra)
        finally:
            # Clean up the temporary file
            os.remove(file_path)

    @classmethod
    async def save_interactions_to_db(cls, interactions:  List[Dict[str, str]]):
        length_metric = LengthMetric()
        for interaction in interactions:
            try:
                result = cls.collection.insert_one(interaction)
                interaction_id = result.inserted_id

                # create and save metrics for this interaction
                # we can add as many metric types as we want to, simply attach it to an interaction via the interaction _id
                input_length = length_metric.calculate(interaction["input"])
                output_length = length_metric.calculate(interaction["output"])
                metric_result = {
                    "interaction_id": str(interaction_id),
                    "metric_name": length_metric.name,
                    "input_value": input_length,
                    "output_value": output_length
                }
                MetricService.create_metric(metric_result)
                alerts = length_metric.alert_checker(metric_result)
                alerts and AlertService.create_alerts(alerts)
            except Exception as e:
                extra = {"traceback": traceback.format_exc(), "error": str(e)}
                CustomLogger.error("Saving interaction to DB", extra=extra)

    @classmethod
    def list_interactions(cls, query):
        return cls.collection.find(query)
