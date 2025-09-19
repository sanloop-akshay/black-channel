import redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD or None,  
    decode_responses=True
)

storage_uri=f"redis://{redis_client.connection_pool.connection_kwargs['host']}:{redis_client.connection_pool.connection_kwargs['port']}/{redis_client.connection_pool.connection_kwargs['db']}"