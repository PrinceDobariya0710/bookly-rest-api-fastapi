from datetime import datetime
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

from src.constants import USER_ROLE


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the user account"},
        )
    )

    username: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    role: str = Field(sa_column=Column(pg.VARCHAR,nullable=False, server_default=USER_ROLE))
    is_verified: bool = False
    email: str
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))

    def __repr__(self) -> str:
        return f"<User {self.username}>"