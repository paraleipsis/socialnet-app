from fastapi import APIRouter

from auth.auth import auth_backend, fastapi_users
from auth.schemas.schemas_user import UserCreate, UserRead


def init_auth_routes() -> APIRouter:
    """Include routes router with prefix '/auth'."""

    router = APIRouter(
        prefix='/auth',
    )

    router.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix='',
        tags=['Auth']
    )
    router.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix='',
        tags=['Auth']
    )

    return router
