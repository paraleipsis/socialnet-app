from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas.schemas_auth import AuthConfig
from db.session import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


def get_auth_config() -> AuthConfig:
    return AuthConfig()
