import json
import pika

from core.config import settings


class QueueProducer:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            credentials = pika.PlainCredentials(
                settings.rabbitmq_user,
                settings.rabbitmq_password,
            )
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.rabbitmq_host,
                    port=settings.rabbitmq_port,
                    credentials=credentials,
                )
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue="processing", durable=True)
            return True
        except Exception as e:
            print(f"Ошибка подключения к RabbitMQ: {e}")
            return False

    def send_product_task(self, task: str, product_id: int, data: dict):
        if self.channel is None or self.connection is None or self.connection.is_closed:
            if not self.connect():
                return False
        try:
            message = {"task": task, "product_id": product_id, **data}
            self.channel.basic_publish(
                exchange="",
                routing_key="processing",
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2),
            )
            print(f"Задача отправлена в очередь: {message}")
            return True
        except Exception as e:
            print(f"Ошибка отправки задачи: {e}")
            return False

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()


producer = QueueProducer()
