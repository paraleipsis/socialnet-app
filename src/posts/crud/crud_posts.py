from typing import Any, Sequence

from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, Row, RowMapping, func, update, delete

from auth.models import User
from modules.cache.key_builders import regular_crud_func_key_builder
from posts.conf import cache_conf
from posts.models import models_posts
from posts.schemas.schemas_posts import PostCreate, PostVotesRead


@cache(
    namespace="votes",
    expire=cache_conf.votes_cache_expire,
    key_builder=regular_crud_func_key_builder
)
async def get_likes_from_db(
    post_id: int,
    session: AsyncSession
) -> int:
    query = select(
        func.count(models_posts.post_likes.c.post_id).label("likes"),
    ).where(
        models_posts.post_likes.c.post_id == post_id
    )

    result = await session.execute(query)
    likes = result.scalars().first()

    return likes


@cache(
    namespace="votes",
    expire=cache_conf.votes_cache_expire,
    key_builder=regular_crud_func_key_builder
)
async def get_dislikes_from_db(
    post_id: int,
    session: AsyncSession
) -> int:
    query = select(
        func.count(models_posts.post_dislikes.c.post_id).label("dislikes"),
    ).where(
        models_posts.post_dislikes.c.post_id == post_id
    )

    result = await session.execute(query)
    dislikes = result.scalars().first()

    return dislikes


async def get_post_by_id(
    post_id: int,
    session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    query = select(
        models_posts.Post,
    ).where(
        models_posts.Post.id == post_id
    )

    result = await session.execute(query)
    post = result.scalars().first()

    return post


async def get_all_posts_from_db(
    session: AsyncSession,
    limit: int = 9,
    skip: int = 0
) -> list[PostVotesRead]:
    query = select(
        models_posts.Post,
        func.count(
            models_posts.post_likes.c.post_id
        ).label("likes"),
        func.count(
            models_posts.post_dislikes.c.post_id
        ).label("dislikes")
    ).join(
        models_posts.post_likes,
        models_posts.post_likes.c.post_id == models_posts.Post.id,
        isouter=True
    ).join(
        models_posts.post_dislikes,
        models_posts.post_dislikes.c.post_id == models_posts.Post.id,
        isouter=True
    ).group_by(
        models_posts.Post.id
    ).limit(
        limit
    ).offset(
        skip
    )

    result = await session.execute(query)
    posts = result.fetchall()
    post_read = [
        PostVotesRead(
            likes=post.likes,
            dislikes=post.dislikes,
            **post.Post.__dict__
        )
        for post in posts
    ]
    return post_read


async def create_post_in_db(
    session: AsyncSession,
    new_post: PostCreate,
    user: User
) -> int:
    query = insert(
        models_posts.Post
    ).values(
        user_id=user.id,
        **new_post.dict()
    ).returning(
        models_posts.Post.id
    )

    result = await session.execute(query)
    await session.commit()

    post_id = result.scalar()

    return post_id


async def update_post_in_db(
    session: AsyncSession,
    post_id: int,
    updated_post: PostCreate,
    user: User
) -> int:
    query = update(
        models_posts.Post
    ).where(
        models_posts.Post.id == post_id,
        models_posts.Post.user_id == user.id
    ).values(
        **updated_post.dict()
    ).returning(
        models_posts.Post.id
    )

    result = await session.execute(query)
    await session.commit()

    post_id = result.scalar()

    return post_id


async def delete_post_in_db(
    session: AsyncSession,
    post_id: int,
    user: User
) -> bool | None:
    query = delete(
        models_posts.Post
    ).where(
        models_posts.Post.id == post_id,
        models_posts.Post.user_id == user.id
    ).returning(
        models_posts.Post.id
    )

    result = await session.execute(query)
    await session.commit()

    post = result.scalar()

    if post is None:
        return None

    return True


async def create_like_in_db(
    session: AsyncSession,
    user: User,
    post_id: int,
) -> bool:
    query = insert(
        models_posts.post_likes
    ).values(
        user_id=user.id,
        post_id=post_id
    )

    await session.execute(query)
    await session.commit()

    return True


async def get_user_post_like_in_db(
    session: AsyncSession,
    user: User,
    post_id: int,
) -> Sequence[Row | RowMapping | Any]:
    query = select(
        models_posts.post_likes
    ).filter(
        models_posts.post_likes.c.post_id == post_id,
        models_posts.post_likes.c.user_id == user.id
    )

    result = await session.execute(query)
    like = result.scalars().first()

    return like


async def delete_user_post_like_in_db(
    session: AsyncSession,
    post_id: int,
    user: User
) -> bool:
    query = delete(
        models_posts.post_likes
    ).where(
        models_posts.post_likes.c.post_id == post_id,
        models_posts.post_likes.c.user_id == user.id
    )

    await session.execute(query)
    await session.commit()

    return True


async def create_dislike_in_db(
    session: AsyncSession,
    user: User,
    post_id: int,
) -> bool:
    query = insert(
        models_posts.post_dislikes
    ).values(
        user_id=user.id,
        post_id=post_id
    )

    await session.execute(query)
    await session.commit()

    return True


async def get_user_post_dislike_in_db(
    session: AsyncSession,
    post_id: int,
    user: User
) -> Sequence[Row | RowMapping | Any]:
    query = select(
        models_posts.post_dislikes
    ).filter(
        models_posts.post_dislikes.c.post_id == post_id,
        models_posts.post_dislikes.c.user_id == user.id
    )

    result = await session.execute(query)
    like = result.scalars().first()

    return like


async def delete_user_post_dislike_in_db(
    session: AsyncSession,
    post_id: int,
    user: User
) -> bool:
    query = delete(
        models_posts.post_dislikes
    ).where(
        models_posts.post_dislikes.c.post_id == post_id,
        models_posts.post_dislikes.c.user_id == user.id
    )

    await session.execute(query)
    await session.commit()

    return True
