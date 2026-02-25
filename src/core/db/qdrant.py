from gc import collect

from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Batch, Distance, VectorParams

from core.config import settings
from feature_pipeline.models.base import VectorDBDataModel

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
                distance=Distance.COSINE,
            ),
        )

    def write_data(self, collection_name: str, points: Batch):
        try:
            self._instance.upsert(collection_name=collection_name, points=points)
        except Exception:
            print("An error occurred while writing data to Qdrant.")

            raise

    def search(
        self,
        collection_name: str,
        query_vector: list,
        query_filter: models.Filter | None = None,
        limit: int = 3,
    ) -> list:
        return self._instance.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
        )

    def scroll(self, collection_name: str, limit: int):
        return self._instance.scroll(collection_name=collection_name, limit=limit)

    def close(self):
        if self._instance:
            self._instance.close()

            print("connection to database closed")


if __name__ == "__main__":
    connection = QdrantDatabaseConnector()
    connection.create_vector_collection("articles") if not connection._instance.collection_exists("articles") else None
    print(connection.get_collection("articles"))
    # connection.write_data(
    #     "articles",
    #     [
    #         VectorDBDataModel(id="1", type="articles", vector=[1.0, 2.0], payload={"title": "test"}),
    #         VectorDBDataModel(id="2", type="articles", vector=[3.0, 4.0], payload={"title": "test2"}),
    #     ],
    # )
    # print(connection.search("articles", [1.0, 2.0]))
    # print(connection.scroll("articles", 2))
    connection.close()
