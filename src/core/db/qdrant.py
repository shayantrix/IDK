from gc import collect

from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Batch, Distance, VectorParams

from core.config import settings


class QdrantDatabaseConnector:
    _instance: QdrantClient | None = None

    def __init__(self) -> None:
        if self._instance == None:
            if settings.USE_QDRANT_CLOUD:
                self._instance = QdrantClient(
                    url=settings.QDRANT_CLOUD_URL,
                    api_key=settings.QDRANT_APIKEY,
                )
            else:
                self._instance = QdrantClient(
                    host=settings.QDRANT_DATABASE_HOST,
                    port=settings.QDRANT_DATABASE_PORT,
                )

    def get_collection(self, collection_name: str):
        return self._instance.get_collection(collection_name=collection_name)

    def create_non_vector_collection(self, collection_name: str):
        self._instance.create_collection(
            collection_name=collection_name, vectors_config={}
        )

    def create_vector_collection(self, collection_name: str):
        self._instance.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=settings.EMBEDDING_SIZE,
            ),
        )
