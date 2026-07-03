import json
import sys
from pathlib import Path

from comet_ml import Artifact, start
from sklearn.model_selection import train_test_split

from core.db.qdrant import QdrantDatabaseConnector

from .chunk_documents import chunk_documents
from .file_handler import FileHandler
from .llm_communication import LLMCommunication

ROOT_DIR = str(Path(__file__).parent.parent.parent)
sys.path.append(ROOT_DIR)

from core.config import settings

settings.patch_localhost()
