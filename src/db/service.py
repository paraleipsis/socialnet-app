from db.schemas.schemas_cache import CacheConfig
from db.schemas.schemas_db import DatabaseConfig


def get_db_config() -> DatabaseConfig:
    return DatabaseConfig()


def get_cache_config() -> CacheConfig:
    return CacheConfig()
