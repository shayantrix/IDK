from core.db.qdrant import QdrantDatabaseConnector
from core.rag.query_expansion import QueryExpansion
from sentence_transformers.SentenceTransformer import SentenceTransformer
from config import settings
from core.rag.prompt_templates import SelfQueryTemplate


class VectorRetrieve:
    """
    for retrieving vectors from a Vector store in a RAG system using query expansion and Multitenancy search
    """

    def __init__(self, query: str) -> None:
        self._client = QdrantDatabaseConnector()
        self.query = query
        self._embedder = SentenceTransformer(settings.EMBEDDING_MODEL_ID)
        self._query_expander = QueryExpansion()
        self._metadata_extractor = SelfQueryTemplate()
        self._reranker = Reranker()