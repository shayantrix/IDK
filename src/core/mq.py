# handles rabbitmq connection
from typing import Self

import pika
from .config import settings

class RabitmqConnection:
    """Singleton class to manage RabbitMQ connection."""

    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host: str | None = None, port: int | None = None,
        username: str | None = None, password: str | None = None,
        virtual_host: str = "/", fail_silently: bool = False,
        **kwargs) -> None:
            self.host = host or settings.RABBITMQ_HOST
            self.port = port or settings.RABBITMQ_PORT
            self.username = username or settings.RABBITMQ_DEFAULT_USERNAME
            self.password = password or settings.RABBITMQ_DEFAULT_PASSWORD
            self.virtual_host = virtual_host
            self.fail_silently = fail_silently
            self.connection = None

    def __enter__(self):
        self.connect()
        return self
