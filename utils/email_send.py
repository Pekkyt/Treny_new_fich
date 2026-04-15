import time


def send_confirmation_email(order_id: int, email: str):
    time.sleep(5)
    print(
        f"Подтвержедение о создании заказа {order_id} было отправлено на почту {email}"
    )
