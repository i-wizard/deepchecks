from pymongo import MongoClient

from app.config.settings import settings


uri = settings.MONGO_URI or settings.DATABASE_URL
client = MongoClient(uri)
db = client["deepchecks_db"]
