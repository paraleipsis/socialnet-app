from typing import Optional

from fastapi import Request, Depends
from fastapi_users import BaseUserManager, UUIDIDMixin, schemas, models, exceptions
from starlette.responses import Response

from auth.exceptions import EmailExistenceError
from auth.models import User
from auth.schemas.schemas_auth import AuthConfig

from auth.service import get_user_db, get_auth_config
from modules.clearbit.clearbit import ClearbitHandler
from modules.hunter_io.hunter import HunterHandler
from modules.logger.logs import logger

auth_conf: AuthConfig = get_auth_config()


class UserManager(UUIDIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = auth_conf.secret_key
    verification_token_secret = auth_conf.secret_key
    hunter_api_key = auth_conf.hunterio_api_key
    clearbit_api_key = auth_conf.clearbit_api_key
    if hunter_api_key not in (None, 'changeme', ''):
        hunterio = HunterHandler(
            api_key=hunter_api_key
        )
    else:
        hunterio = None

    if clearbit_api_key not in (None, 'changeme', ''):
        clearbit = ClearbitHandler(
            api_key=clearbit_api_key
        )
    else:
        clearbit = None

    async def on_after_register(
            self,
            user: User,
            request: Optional[Request] = None
    ):
        logger['debug'].debug(
            f"User {user.id} has registered."
        )

    async def on_after_forgot_password(
            self,
            user: User,
            token: str,
            request: Optional[Request] = None
    ):
        logger['debug'].debug(
            f"User {user.id} has forgot their password. Reset token: {token}"
        )

    async def on_after_request_verify(
            self,
            user: User,
            token: str,
            request: Optional[Request] = None
    ):
        logger['debug'].debug(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )

    async def on_after_login(
            self,
            user: User,
            request: Optional[Request] = None,
            response: Optional[Response] = None,
    ):
        logger['debug'].debug(
            f"User {user.id} logged in."
        )

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )

        if UserManager.hunterio is not None:
            hunter_response = await UserManager.hunterio.email_verifier(
                email=user_dict['email']
            )
            if not hunter_response['regexp'] and not hunter_response['smtp_check']:
                raise EmailExistenceError('Email does not exist')

        if UserManager.clearbit is not None:
            try:
                clearbit_response = await UserManager.clearbit.email_lookup(
                    email=user_dict['email']
                )
                user_dict['first_name'] = clearbit_response['name']['givenName']
                user_dict['last_name'] = clearbit_response['name']['familyName']
            except Exception as exc:
                logger['debug'].debug(
                    f'Error getting full name with Clearbit API: {repr(exc)}'
                )

        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
