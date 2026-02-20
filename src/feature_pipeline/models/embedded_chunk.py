from typing import Tuple

import numpy as np
from models.base import VectorDBDataModel


class ArticleEmbeddedChunkModel(VectorDBDataModel):
    entry_id: str
    platform: str
    link: str
    chunk_id: str
    chunk_content: str
    embedded_content: np.ndarray
    author_id: str
    type: str

    class Config:
        arbitrary_types_allowed = True

    def to_payload(self) -> Tuple[str, np.ndarray, dict]:
        data = {
            "id": self.entry_id,
            "platform": self.platform,
            "link": self.link,
            "chunk_content": self.chunk_content,
            "author_id": self.author_id,
            "type": self.type,
        }

        return self.chunk_id, self.embedded_content, data
