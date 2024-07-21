from pathlib import Path
import os

from dotenv import load_dotenv

env_path = Path().absolute()/'.env'
load_dotenv(dotenv_path=env_path)


#  Singleton class to hold project settings
class Settings:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance

    DB_USER = os.environ.get("MONGO_INITDB_ROOT_USERNAME", "root")
    DB_PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD", "password")
    DB_PORT = os.environ.get("MONGO_DB_PORT", 27017)
    DATABASE_URL = f"mongodb://{DB_USER}:{DB_PASSWORD}@mongodb:{DB_PORT}/"
    MONGO_URI = os.environ.get("MONGO_URI")
    REDIS_HOST = os.environ.get("REDIS_HOST", 'redis')
    REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
    LENGTH_METRIC_THRESHOLD = {k: int(v) for k, v in zip(
        ["minimum", "maximum"], os.environ.get('LENGTH_METRIC_THRESHOLD', '1,3').split(","))}  # output {'minimum': 1, 'maximum': 2}


settings: Settings = Settings()
