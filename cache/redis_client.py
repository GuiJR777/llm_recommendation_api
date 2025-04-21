import redis
import json
import hashlib
from utils.logger import logger
from utils.config import REDIS_HOST, REDIS_PORT, REDIS_DB, CACHE_TTL_SECONDS

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


def cache_result(ttl=CACHE_TTL_SECONDS, factory=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not redis_available:
                return func(*args, **kwargs)

            try:
                key = make_cache_key(func.__name__, *args, **kwargs)
                cached = redis_client.get(key)
                if cached:
                    logger.info(f"Cache HIT: {key}")
                    data = json.loads(cached)
                    if factory:
                        return [factory(**item) for item in data]
                    return data

                logger.info(f"Cache MISS: {key}")
                result = func(*args, **kwargs)
                redis_client.setex(
                    key, ttl, json.dumps([r.__dict__ for r in result])
                )
                return result

            except redis.RedisError as e:
                logger.error(f"Erro ao acessar o Redis: {e}")
                return func(*args, **kwargs)

        return wrapper

    return decorator


def clear_all_cache():
    if redis_available:
        redis_client.flushdb()
        logger.info("Cache limpo com sucesso.")
    else:
        logger.warning("Tentativa de limpar cache sem Redis disponível.")
