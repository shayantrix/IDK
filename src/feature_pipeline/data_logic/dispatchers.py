from cleaning_data_handlers import ArticleCleaningHandler, CleaningDataHandler
from models.base import DataModel
from models.raw import ArticleRawModel


class RawDispatcher:
    @staticmethod
    def handle_mq_message(message: dict) -> DataModel:
        data_type = message.get("type")
        if data_type == "article":
            return ArticleRawModel(**message)
        else:
            raise ValueError("unsupported data type")


class CleaningHandlerFactory:
    @staticmethod
    def create_handler(data_type) -> CleaningDataHandler:
        if data_type == "articles":
            return ArticleCleaningHandler()
        else:
            raise ValueError("Unsupported data type")


class CleaningDispatcher:
    cleaning_factory = CleaningHandlerFactory()

    @classmethod
    def dispatch_cleaner(cls, data_model: DataModel) -> DataModel:
        data_type = data_model.type
        handler = cls.cleaning_factory.create_handler(data_type)
        clean_model = handler.clean(data_model)

        return clean_model
