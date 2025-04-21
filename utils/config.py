import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
CACHE_TTL_SECONDS = int(
    os.getenv("CACHE_TTL_SECONDS", 60 * 60 * 72)
)  # 72 horas
