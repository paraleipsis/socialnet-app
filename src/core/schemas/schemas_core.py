from pydantic import BaseSettings
from conf.config import BASE_DIR

db_conf_dir = "core/conf/core"


class CoreConfig(BaseSettings):
    host: str
    port: int
    log_level: str
    docs_url: str
    openapi_url: str
    title: str

    class Config:
        env_file = BASE_DIR / db_conf_dir
