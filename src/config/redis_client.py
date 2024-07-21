import redis

from src.config.settings import settings

redis_client = redis.Redis(host=settings.REDIS_HOST,
                           port=settings.REDIS_PORT, db=0)
