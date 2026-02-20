from typing import Optional

from models.base import DataModel


class ArticleChunkModel(DataModel):
    entry_id: str
    platform: str
    link: str
    chunk_id: str
    chunk_content: str
    author_id: str
    type: str
