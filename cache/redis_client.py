import redis
import json
import hashlib
from functools import wraps
from typing import Optional, Type, Any, Callable
from utils.logger import logger
from utils.config import REDIS_HOST, REDIS_PORT, REDIS_DB, CACHE_TTL_SECONDS

# Redis connection
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    redis_client.ping()
    redis_available = True
    logger.info("Conectado ao Redis com sucesso.")
except redis.RedisError as e:
    redis_client = None
    redis_available = False
    logger.warning(f"Falha ao conectar ao Redis: {e}. Cache será ignorado.")


def make_cache_key(function_name: str, *args, **kwargs) -> str:
    key_raw = f"{function_name}:{args}:{kwargs}"
    return hashlib.sha256(key_raw.encode()).hexdigest()


def serialize_result(result: Any) -> str:
    if isinstance(result, list):
        return json.dumps([r.__dict__ for r in result])
    elif isinstance(result, str):
        return json.dumps(result)
    elif result is None:
        return json.dumps(None)
    else:
        return json.dumps(result.__dict__)


def deserialize_result(cached: str, factory: Optional[Type]) -> Any:
    data = json.loads(cached)
    if factory:
        return [factory(**item) for item in data]
    return data


def handle_cache(
    func: Callable, ttl: int, factory: Optional[Type], is_async: bool
):
    if is_async:

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if not redis_available:
                return await func(*args, **kwargs)

            try:
                key = make_cache_key(func.__name__, *args, **kwargs)
                cached = redis_client.get(key)
                if cached:
                    logger.info(f"Cache HIT: {key}")
                    return deserialize_result(cached, factory)

                logger.info(f"Cache MISS: {key}")
                result = await func(*args, **kwargs)
                redis_client.setex(key, ttl, serialize_result(result))
                return result

            except Exception as e:
                logger.warning(f"Erro no cache async: {e}")
                return await func(*args, **kwargs)

        return async_wrapper

    else:

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            if not redis_available:
                return func(*args, **kwargs)

            try:
                key = make_cache_key(func.__name__, *args, **kwargs)
                cached = redis_client.get(key)
                if cached:
                    logger.info(f"Cache HIT: {key}")
                    return deserialize_result(cached, factory)

                logger.info(f"Cache MISS: {key}")
                result = func(*args, **kwargs)
                redis_client.setex(key, ttl, serialize_result(result))
                return result

            except Exception as e:
                logger.warning(f"Erro no cache sync: {e}")
                return func(*args, **kwargs)

        return sync_wrapper


def cache_result(ttl: int = CACHE_TTL_SECONDS, factory: Optional[Type] = None):
    return lambda func: handle_cache(func, ttl, factory, is_async=False)


def async_cache_result(
    ttl: int = CACHE_TTL_SECONDS, factory: Optional[Type] = None
):
    return lambda func: handle_cache(func, ttl, factory, is_async=True)


def clear_all_cache():
    if redis_available:
        redis_client.flushdb()
        logger.info("Cache limpo com sucesso.")
    else:
        logger.warning("Tentativa de limpar cache sem Redis disponível.")
