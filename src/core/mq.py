# handles rabbitmq connection
from typing import Self

import pika

from .config import settings


class RabbitMQConnection:
    """Singleton class to manage RabbitMQ connection."""

    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        virtual_host: str = "/",
        fail_silently: bool = False,
        **kwargs,
    ) -> None:
        self.host = host or settings.RABBITMQ_HOST
        self.port = port or settings.RABBITMQ_PORT
        self.username = username or settings.RABBITMQ_DEFAULT_USERNAME
        self.password = password or settings.RABBITMQ_DEFAULT_PASSWORD
        self.virtual_host = virtual_host
        self.fail_silently = fail_silently
        self._connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    virtual_host=self.virtual_host,
                    credentials=credentials,
                )
            )
        except pika.exceptions.AMQPConnectionError as e:
            if not self.fail_silently:
                raise e

    def is_connected(self) -> bool:
        return self._connection is not None and self._connection.is_open

    def get_channel(self):
        if self.is_connected():
            return self._connection.channel()

    def close(self):
        if self.is_connected():
            self._connection.close()
            self._connection = None
            print("Closed Rabbitmq connection")


"""The data variable, which is expected to be a JSON string,
represents the changes captured by MongoDB's CDC mechanism."""


def publish_to_rabbitmq(queue_name: str, data: str):
    """publish data to rabbitmq"""
    try:
        rabbitmq_conn = RabbitMQConnection()

        # establish connection
        with rabbitmq_conn:
            channel = rabbitmq_conn.get_channel()

            # ensure the queue exists
            channel.queue_declare(queue=queue_name, durable=True)

            # delivery confirmation
            channel.confirm_delivery()

            # send data to queue
            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=data,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )
    except pika.exceptions.UnroutableError:
        print("Failed to publish message to RabbitMQ")
    except Exception:
        print("Error publishing to RabbitMQ")


if __name__ == "__main__":
    publish_to_rabbitmq("test my queue", "hail shayan the great")
