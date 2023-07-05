from sqlalchemy import Column, String, TIMESTAMP, Integer, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text

from db.database import metadata, Base

post_likes = Table(
    "likes", metadata,
    # Column("id", Integer, primary_key=True, index=True),
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
)

post_dislikes = Table(
    "dislikes", metadata,
    # Column("id", Integer, primary_key=True, index=True),
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
)


class Post(Base):
    __tablename__ = "posts"
    metadata = metadata

    id: int = Column(Integer, primary_key=True, nullable=False)
    title: str = Column(String, nullable=False)
    content: str = Column(String, nullable=False)
    created_at: TIMESTAMP = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id: UUID = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
