import json
import time
import pika

from core.config import settings
from services.products.dependencies import (
    report_created_product,
    send_email_with_created_order,
)


class QueueConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.max_retries = 3

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
            self.channel.queue_declare(queue="processing_errors", durable=True)
            self.channel.basic_qos(prefetch_count=1)
            return True
        except Exception as e:
            print(f"Ошибка подключения consumer к RabbitMQ: {e}")
            return False

    def process_message(self, ch, method, properties, body):
        retry_count = (
            properties.headers.get("x-retry-count", 0) if properties.headers else 0
        )

        try:
            message = json.loads(body)
            task = message["task"]
            product_id = message["product_id"]

            if task == "send_email":
                send_email_with_created_order(
                    user_email=message["user_email"],
                    product_id=product_id,
                )
            elif task == "report":
                report_created_product(
                    product_id=product_id,
                    product_price=message["product_price"],
                    user_id=int(message["user_id"]),
                )

            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"Задача {task} для продукта {product_id} обработана")
        except Exception as e:
            print(f"Ошибка обработки задачи: {e}")

            if retry_count < self.max_retries:
                retry_count += 1
                time.sleep(2**retry_count)
                ch.basic_publish(
                    exchange="",
                    routing_key="processing",
                    body=body,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        headers={"x-retry-count": retry_count},
                    ),
                )
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            else:
                ch.basic_publish(
                    exchange="",
                    routing_key="processing_errors",
                    body=body,
                    properties=pika.BasicProperties(delivery_mode=2),
                )
                ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        if not self.connect():
            return

        self.channel.basic_consume(
            queue="processing",
            on_message_callback=self.process_message,
        )
        print("Ожидание сообщений в очереди processing")

        try:
            self.channel.start_consuming()
        except Exception as e:
            print(f"Ошибка consumer: {e}")
        finally:
            if self.connection and not self.connection.is_closed:
                self.connection.close()


consumer = QueueConsumer()
