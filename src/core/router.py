from fastapi import FastAPI, APIRouter

from auth.router import init_auth_routes
from posts.api.api_posts import router as posts_routes


def init_v1_routes() -> APIRouter:
    """Include routes in all apps to router with prefix '/v1'."""

    router = APIRouter(
        prefix='/v1',
    )

    auth_routes = init_auth_routes()
    router.include_router(auth_routes)

    router.include_router(posts_routes)

    return router


def init_api_routes(application: FastAPI) -> None:
    """Include routes in all apps to core router with prefix '/api'.

        :param application:
            The :class:`FastAPI` application.

    """

    api_router = APIRouter(
        prefix='/api',
    )

    v1_routes = init_v1_routes()

    api_router.include_router(v1_routes)

    # main
    application.include_router(api_router)

    return None
