from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core import middleware
from core.router import init_api_routes
from core.schemas.schemas_core import CoreConfig
from core.service import get_core_config
from core.startup_tasks.redis_conn import redis_connect
from modules.exc.exc import init_exc_handlers

core_conf: CoreConfig = get_core_config()


def pre_startup(application: FastAPI) -> None:
    init_exc_handlers(application=application)
    init_api_routes(application=application)


async def startup() -> None:
    redis_connect()


async def shutdown() -> None:
    pass


def create_app() -> FastAPI:
    application = FastAPI(
        title=core_conf.title,
        docs_url=core_conf.docs_url,
        openapi_url=core_conf.openapi_url,
        middleware=middleware.utils,
        on_startup=[startup],
        on_shutdown=[shutdown]
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    pre_startup(application)

    return application


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=core_conf.host,
        port=core_conf.port,
        log_level=core_conf.log_level,
        reload=True
    )
