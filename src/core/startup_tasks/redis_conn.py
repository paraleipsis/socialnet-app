from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from db.schemas.schemas_cache import CacheConfig
from db.service import get_cache_config


def redis_connect():
    cache_conf: CacheConfig = get_cache_config()
    redis_conn = aioredis.from_url(
        f"redis://{cache_conf.redis_host}:{cache_conf.redis_port}"
    )
    FastAPICache.init(
        RedisBackend(redis_conn),
        prefix=f"{cache_conf.cache_prefix}"
    )
