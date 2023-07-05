from pydantic import BaseSettings
from conf.config import BASE_DIR

cache_conf_dir = "db/conf/cache"


class CacheConfig(BaseSettings):
    redis_host: str
    redis_port: str
    cache_prefix: str
    votes_cache_expire: int

    class Config:
        env_file = BASE_DIR / cache_conf_dir
