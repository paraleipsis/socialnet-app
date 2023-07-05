import hashlib
from typing import Optional

from fastapi_cache import FastAPICache
from starlette.requests import Request
from starlette.responses import Response


def regular_crud_func_key_builder(
    fnc,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"

    arguments = {}
    for key, value in kwargs.items():
        if key != 'session':
            arguments[key] = value
    cache_key = prefix + hashlib.md5(f"{fnc.__module__}:{fnc.__name__}:{args}:{arguments}".encode()).hexdigest()

    return cache_key
