from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from auth.models import User
from db.session import get_async_session
from modules.schemas.schemas_response import GenericResponseModel
from posts.schemas import schemas_posts
from posts.service import service_posts
from auth.auth import current_user


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get(
    '/{post_id}',
    response_model=GenericResponseModel[schemas_posts.PostVotesRead]
)
async def get_post_request(
        post_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_posts.get_post(
        session=session,
        post_id=post_id
    )


@router.get(
    '/',
    response_model=GenericResponseModel[List[schemas_posts.PostVotesRead]]
)
async def get_all_posts_request(
        session: AsyncSession = Depends(get_async_session),
        limit: Optional[int] = 9,
        skip: Optional[int] = 0
):
    return await service_posts.get_all_posts(
        session=session,
        limit=limit,
        skip=skip
    )


@router.post(
    '/',
    response_model=GenericResponseModel[schemas_posts.PostRead]
)
async def create_post_request(
        new_post: schemas_posts.PostCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await service_posts.create_post(
        session=session,
        new_post=new_post,
        user=user
    )


@router.put(
    '/{post_id}',
    response_model=GenericResponseModel[schemas_posts.PostVotesRead]
)
async def update_post_request(
        post_id: int,
        updated_post: schemas_posts.PostCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await service_posts.update_post(
        session=session,
        post_id=post_id,
        updated_post=updated_post,
        user=user
    )


@router.delete(
    '/{post_id}',
    response_model=GenericResponseModel[bool]
)
async def delete_post_request(
        post_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await service_posts.delete_post(
        session=session,
        post_id=post_id,
        user=user
    )


@router.post(
    '/{post_id}/like',
    response_model=GenericResponseModel[bool]
)
async def like_post_request(
        post_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await service_posts.like_post(
        session=session,
        post_id=post_id,
        user=user,
    )


@router.post(
    '/{post_id}/dislike',
    response_model=GenericResponseModel[bool]
)
async def dislike_post_request(
        post_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await service_posts.dislike_post(
        session=session,
        post_id=post_id,
        user=user,
    )
