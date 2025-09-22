# app/core/settings.py or wherever you keep settings
from celery import Celery
from app.core.config import settings
import redis

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD or None,  
    decode_responses=True
)

storage_uri = f"redis://{redis_client.connection_pool.connection_kwargs['host']}:{redis_client.connection_pool.connection_kwargs['port']}/{redis_client.connection_pool.connection_kwargs['db']}"

celery_app = Celery(
    "black_channel",
    broker=storage_uri,
    backend=storage_uri
)

celery_app.conf.task_routes = {
    "tasks.mailer_task.*": {"queue": "mail_queue"},
}
