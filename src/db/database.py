from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta
from sqlalchemy.pool import NullPool

from db.schemas.schemas_db import DatabaseConfig
from db.service import get_db_config


db_config: DatabaseConfig = get_db_config()
DATABASE_URL = f"postgresql+asyncpg://{db_config.postgres_user}:{db_config.postgres_password}@" \
               f"{db_config.postgres_host}:{db_config.postgres_port}/{db_config.postgres_db}"

engine = create_async_engine(
    url=DATABASE_URL,
    poolclass=NullPool
)

Base: DeclarativeMeta = declarative_base()
metadata = MetaData()

# noinspection PyTypeChecker
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
