from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from modules.exc.exceptions.posts import NoSuchPost, UserVoteError
from modules.schemas.schemas_response import GenericResponseModel
from posts.crud import crud_posts
from posts.schemas.schemas_posts import PostVotesRead


async def get_post(
        session: AsyncSession,
        post_id: int,
) -> GenericResponseModel:
    post = await crud_posts.get_post_by_id(
        session=session,
        post_id=post_id,
    )

    if not post:
        raise NoSuchPost(f'Post with id {post_id} does not exist')

    likes = await crud_posts.get_likes_from_db(
        session=session,
        post_id=post_id,
    )

    dislikes = await crud_posts.get_dislikes_from_db(
        session=session,
        post_id=post_id,
    )

    post_votes = PostVotesRead(likes=likes, dislikes=dislikes, **post.__dict__)

    return GenericResponseModel(data=post_votes, total=1)


async def get_all_posts(
        session: AsyncSession,
        **kwargs
) -> GenericResponseModel:
    data = await crud_posts.get_all_posts_from_db(
        session=session,
        **kwargs
    )

    return GenericResponseModel(data=data, total=len(data))


async def create_post(
        session: AsyncSession,
        **kwargs
) -> GenericResponseModel:
    post_id = await crud_posts.create_post_in_db(
        session=session,
        **kwargs
    )

    post = await crud_posts.get_post_by_id(
        session=session,
        post_id=post_id
    )

    return GenericResponseModel(data=post, total=1)


async def update_post(
        session: AsyncSession,
        post_id: int,
        **kwargs
) -> GenericResponseModel:
    updated_post_id = await crud_posts.update_post_in_db(
        session=session,
        post_id=post_id,
        **kwargs
    )

    if not updated_post_id:
        raise NoSuchPost(f'Post with id {post_id} does not exist')

    post = await crud_posts.get_post_by_id(
        session=session,
        post_id=updated_post_id
    )

    return GenericResponseModel(data=post, total=1)


async def delete_post(
        session: AsyncSession,
        post_id: int,
        **kwargs
) -> GenericResponseModel:
    result = await crud_posts.delete_post_in_db(
        session=session,
        post_id=post_id,
        **kwargs
    )

    if not result:
        raise NoSuchPost(f'Post with id {post_id} does not exist')

    return GenericResponseModel(data=result, total=1)


async def like_post(
    session: AsyncSession,
    post_id: int,
    user: User
) -> GenericResponseModel:
    post = await get_post(
        session=session,
        post_id=post_id
    )

    if post.data.user_id == user.id:
        raise UserVoteError('User cannot rate their own posts')

    is_liked = await crud_posts.get_user_post_like_in_db(
        session=session,
        post_id=post_id,
        user=user
    )

    is_disliked = await crud_posts.get_user_post_dislike_in_db(
        session=session,
        post_id=post_id,
        user=user
    )

    if is_liked:
        data = await crud_posts.delete_user_post_like_in_db(
            session=session,
            post_id=post_id,
            user=user
        )

        return GenericResponseModel(data=data, total=1)

    if is_disliked:
        await crud_posts.delete_user_post_dislike_in_db(
            session=session,
            post_id=post_id,
            user=user
        )

    data = await crud_posts.create_like_in_db(
        session=session,
        post_id=post_id,
        user=user
    )

    return GenericResponseModel(data=data, total=1)


async def dislike_post(
    session: AsyncSession,
    post_id: int,
    user: User
) -> GenericResponseModel:
    post = await get_post(
        session=session,
        post_id=post_id
    )

    if post.data.user_id == user.id:
        raise UserVoteError('User cannot rate their own posts')

    is_disliked = await crud_posts.get_user_post_dislike_in_db(
        session=session,
        post_id=post_id,
        user=user
    )

    is_liked = await crud_posts.get_user_post_like_in_db(
        session=session,
        post_id=post_id,
        user=user
    )

    if is_disliked:
        data = await crud_posts.delete_user_post_dislike_in_db(
            session=session,
            post_id=post_id,
            user=user
        )

        return GenericResponseModel(data=data, total=1)

    if is_liked:
        await crud_posts.delete_user_post_like_in_db(
            session=session,
            post_id=post_id,
            user=user
        )

    await get_post(
        session=session,
        post_id=post_id
    )

    data = await crud_posts.create_dislike_in_db(
        session=session,
        post_id=post_id,
        user=user
    )

    return GenericResponseModel(data=data, total=1)
