# connection of monogo db
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from core.config import settings

class MongoDatabaseConnector:
    _instance: MongoClient | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            try:
                cls._instance = MongoClient(settings.MONGO_DATABASE_HOST)
            except ConnectionFailure:
                raise ConnectionFailure("Failed to connect to MongoDB")
        return cls._instance

    def get_database(self):
        # assertion if not true raise an error
        assert self._instance, "Database Connection not initialized"
        return self._instance[settings.MONGO_DATABASE_NAME]

    def close(self):
        if self._instance:
            self._instance.close()
            print("MongoDB connection closed")

connection = MongoDatabaseConnector()
