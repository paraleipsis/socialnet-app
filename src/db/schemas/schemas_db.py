from pydantic import BaseSettings
from conf.config import BASE_DIR

db_conf_dir = "db/conf/db"


class DatabaseConfig(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str

    class Config:
        env_file = BASE_DIR / db_conf_dir
