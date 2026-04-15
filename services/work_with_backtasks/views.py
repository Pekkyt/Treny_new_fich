from fastapi import APIRouter, HTTPException, status
from fastapi.background import BackgroundTasks
from utils.email_send import send_confirmation_email
import uuid
from .schemas import OrderCreate
import time

router = APIRouter(tags=["BACK_TASKS"], prefix="/back_tasks")

task_statuses: dict[str, dict] = {}


# ====================  1  =================================================================
@router.post("/orders/{order_id}/confirm")
async def confirm_order(order_id: int, background_tasks: BackgroundTasks):
    email = "me@example.com"
    background_tasks.add_task(send_confirmation_email, order_id, email)
    return {"order_id": order_id, "status": "confirmed"}


# ====================  2  =================================================================
@router.post("/exports")
async def start_export(background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    task_statuses[task_id] = {"status": "pending"}
    background_tasks.add_task(export_catalog, task_id)
    return {"task_id": task_id, "status": "accepted"}


@router.get("/exports/{task_id}")
async def get_export_status(task_id: str):
    if task_id not in task_statuses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return task_statuses[task_id]


def export_catalog(task_id: str):
    task_statuses[task_id] = {"status": "in_progress"}
    try:
        time.sleep(20)
        task_statuses[task_id]["status"] = "completed"
    except Exception as e:
        task_statuses[task_id] = {"status": "failed", "error": str(e)}


# ====================  3  =================================================================
def send_email(order_id: int, email: str):
    time.sleep(1)
    print(f"Сообщение о покупке заказа {order_id} было отправлено на {email}")


def update_stock(order_id: int, items: list[dict]):
    time.sleep(15)
    for item in items:
        print(f"Заказ #{order_id}: остаток обновлён для товара {item['product_id']}")


def notify_manager(order_id: int, total: float):
    time.sleep(5)
    print(f"Менеджер уведомлен о заказе {order_id} на сумму {total}")


@router.post("/orders")
async def create_order(order: OrderCreate, background_tasks: BackgroundTasks):
    order_id = 42
    background_tasks.add_task(send_email, order_id, order.user_email)
    background_tasks.add_task(update_stock, order_id, order.items)
    background_tasks.add_task(notify_manager, order_id, order.total)
    return {"order_id": order_id, "status": "created"}
