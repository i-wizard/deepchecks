from src.core.models import metric_collection

from src.utils.key_builder import KeyBuilder
from src.utils.cache_manager import CacheManager


class MetricService:
    collection = metric_collection

    @classmethod
    def create_metric(cls, data: dict):
        result = cls.collection.insert_one(data)
        # cache newly added lengths
        cache = CacheManager()
        input_length_key = KeyBuilder.interaction_input_length()
        output_length_key = KeyBuilder.interaction_output_length()
        saved_input_lengths = cache.retrieve_key(
          input_length_key) or []
        saved_output_lengths = cache.retrieve_key(
            output_length_key) or []
        saved_input_lengths.append(data['input_value'])
        cache.set_key(input_length_key, saved_input_lengths)
        saved_output_lengths.append(data['output_value'])
        cache.set_key(output_length_key, saved_output_lengths)

        return result.inserted_id

    @classmethod
    def list_metrics(cls, query):
        return cls.collection.find(query)