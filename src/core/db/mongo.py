# connection of monogo db
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from core.config import settings

class MongoDatabaseConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = None
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        try:
            # MongoClient is lazy, this mostly validates URI shape here.
            self._client = MongoClient(settings.MONGO_DATABASE_HOST)
            self._initialized = True
        except ConnectionFailure as exc:
            raise ConnectionFailure("Failed to connect to MongoDB") from exc

    def get_database(self):
        assert self._client is not None, "Database connection not initialized"
        return self._client[settings.MONGO_DATABASE_NAME]

    def close(self):
        if self._client is not None:
            self._client.close()
            print("MongoDB connection closed")

connection = MongoDatabaseConnector()
