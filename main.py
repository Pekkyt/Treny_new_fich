from fastapi import FastAPI, Request
import time
import logging

"""from services.products.views import process_queue"""
from services.users.views import router as users_router
from services.products.views import router as products_router
from services.external_posts.views import router as external_posts_router
from services.exchange_client.views import router as exchange_client_router
from services.work_with_backtasks.views import router as work_with_backtasks_router
import threading
from contextlib import asynccontextmanager
from services.queue_consumer import consumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    thread = threading.Thread(target=consumer.start_consuming, daemon=True)
    thread.start()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(external_posts_router)
app.include_router(exchange_client_router)
app.include_router(work_with_backtasks_router)


@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Запрос: {request.method} {request.url.path}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Ответ: {response.status_code}, за {process_time:.3f} сек")
    response.headers["X-Process-Time"] = str(process_time)
    return response
