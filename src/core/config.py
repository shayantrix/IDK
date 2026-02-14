from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = str(Path(__file__).parent.parent.parent)

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR, env_file_encoding="utf-8")

    #mongodb
    MONGO_DATABASE_HOST: str = (
        "mongodb://admin:password@localhost:27017/"
    )
    MONGO_DATABASE_NAME: str = "IDK"

    def patch_localhost(self) -> None:
        self.MONGO_DATABASE_HOST = "mongodb://admin:password@localhost:27017/"

    # rabbitmq
    RABBITMQ_DEFAULT_USERNAME: str = "guest"
    RABBITMQ_DEFAULT_PASSWORD: str = "guest"
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672

settings = AppSettings()
