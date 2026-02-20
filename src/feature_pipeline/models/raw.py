from typing import Optional

from models.base import DataModel


class ArticleRawModel(DataModel):
    platform: str
    link: str
    content: str
    author_id: str
