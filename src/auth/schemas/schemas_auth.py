from pydantic import BaseSettings

from conf.config import BASE_DIR

auth_conf_dir = "auth/conf/auth"


class AuthConfig(BaseSettings):
    secret_key: str
    cookie_max_age: int
    jwt_lifetime_seconds: int
    hunterio_api_key: str
    clearbit_api_key: str

    class Config:
        env_file = BASE_DIR / auth_conf_dir
