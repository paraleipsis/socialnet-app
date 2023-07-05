from starlette.requests import Request
from starlette.responses import JSONResponse

from modules.exc.exceptions.posts import NoSuchPost, UserVoteError
from modules.logger.logs import logger
from modules.schemas.schemas_response import GenericResponseModel


async def post_not_exists_exception_handler(
        request: Request,
        exc: NoSuchPost
) -> JSONResponse:
    logger['debug'].debug(
        f'{type(exc).__name__}: {str(exc)}'
    )
    return JSONResponse(
        status_code=404,
        content=GenericResponseModel(success=False, error_msg=str(exc)).dict()
    )


async def user_vote_exception_handler(
        request: Request,
        exc: UserVoteError
) -> JSONResponse:
    logger['debug'].debug(
        f'{type(exc).__name__}: {str(exc)}'
    )
    return JSONResponse(
        status_code=403,
        content=GenericResponseModel(success=False, error_msg=str(exc)).dict()
    )
