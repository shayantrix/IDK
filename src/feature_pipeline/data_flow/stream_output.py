from bytewax.outputs import DynamicSink, StatelessSinkPartition
from qdrant_client.models import Batch

from core.db.qdrant import QdrantDatabaseConnector
from feature_pipeline.models.base import VectorDBDataModel


class QdrantOutput(DynamicSink):
    """
    Bytewax class that facilitates the connection to a Qdrant vector DB
    Inherits from DynamicSink due to ability of creating different sink
    sources (e.x. vector and non-vector collections)
    """

    def __init__(self, connection: QdrantDatabaseConnector, sink_type: str):
        self._connection = connection
        self._sink_type = sink_type

        collections = {
            "cleaned_articles": False,
            "vector_articles": True,
        }

        for collection_name, is_vector in collections.items():
            try:
                self._connection.get_collection(collection_name=collection_name)
            except Exception:
                print(
                    f"Could not access the {collection_name} collection. Creating a new one..."
                )

                if is_vector:
                    self._connection.create_vector_collection(
                        collection_name=collection_name,
                    )
                else:
                    self._connection.create_non_vector_collection(
                        collection_name=collection_name
                    )

    def build(self, worker_index: int, worker_count: int) -> StatelessSinkPartition:
        if self._sink_type == "clean":
            return QdrantCleanedDataSink(connection=self._connection)
        elif self._sink_type == "vector":
            return QdrantVectorDataSink(connection=self._connection)
        else:
            raise ValueError(f"Unsupported sink type: {self._sink_type}")


class QdrantVectorDataSink(StatelessSinkPartition):
    def __init__(self, connection: QdrantDatabaseConnector):
        self._client = connection

    def write_batch(self, items: list[VectorDBDataModel]) -> None:
        payloads = [item.to_payload() for item in items]
        ids, vectors, meta_data = zip(*payloads)
        collection_name = get_vector_collection(data_type=meta_data[0]["type"])
        self._client.write_data(
            collection_name=collection_name,
            points=Batch(ids=ids, vectors=vectors, payloads=meta_data),
        )


class QdrantCleanedDataSink(StatelessSinkPartition):
    def __init__(self, connection: QdrantDatabaseConnector):
        self._client = connection

    def write_batch(self, items: list[VectorDBDataModel]) -> None:
        payloads = [item.to_payload() for item in items]
        ids, data = zip(*payloads)
        collection_name = get_clean_collection(data_type=data[0]["type"])
        self._client.write_data(
            collection_name=collection_name,
            points=Batch(ids=ids, vectors={}, payloads=data),
        )

        print(
            f"Successfuly inserted requested cleaned points(s), {collection_name}, num= {len(ids)}"
        )


def get_clean_collection(data_type: str) -> str:
    if data_type == "articles":
        return "cleaned_articles"
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


def get_vector_collection(data_type: str) -> str:
    if data_type == "articles":
        return "vector_articles"
    else:
        raise ValueError(f"Unsupported data type: {data_type}")
