from abc import ABC, abstractmethod

from models.base import DataModel
from models.clean import ArticleCleanedModel
from models.raw import ArticleRawModel
from utils.cleaning import clean_text

class CleaningDataHandler(ABC):
    """
    Abstract class for all data cleaning handlers
    """
    @abstractmethod
    def clean(self, data_model: DataModel) -> DataModel:
        pass

class ArticleCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: ArticleRawModel) -> ArticleCleanedModel:
        joined_text = (
            "".join(data_model.content.values()) if data_model and data_model.content else None
        )

        return ArticleCleanedModel(
            entry_id=data_model.entry_id,
            platform=data_model.platform,
            link=data_model.link,
            cleaned_content=clean_text(joined_text),
            author_id=data_model.author_id,
            type=data_model.type,
        )

if __name__ == "__main__":
    handler = ArticleCleaningHandler()
    cleaned_data = handler.clean(ArticleRawModel(entry_id="1", platform="test", link="test", content={"test": "test"}, author_id="1", type="articles"))
    print(cleaned_data)
