import uuid

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text

from db.database import metadata, Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    metadata = metadata

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email: str = Column(String, nullable=False, unique=True)
    username: str = Column(String, nullable=False)
    first_name: str = Column(String, nullable=True)
    last_name: str = Column(String, nullable=True)
    registered_at: TIMESTAMP = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
