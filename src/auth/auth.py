from uuid import UUID

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, CookieTransport

from auth.models.models_user import User
from auth.service import get_auth_config
from auth.user_manager import get_user_manager


auth_conf = get_auth_config()

cookie_transport = CookieTransport(
    cookie_max_age=auth_conf.cookie_max_age
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=auth_conf.secret_key,
        lifetime_seconds=auth_conf.jwt_lifetime_seconds
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
