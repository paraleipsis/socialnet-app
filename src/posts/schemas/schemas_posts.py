from uuid import UUID

from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    created_at = datetime


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    user_id: UUID

    class Config:
        orm_mode = True


class PostVotesRead(PostRead):
    likes: int = 0
    dislikes: int = 0

    class Config:
        orm_mode = True
