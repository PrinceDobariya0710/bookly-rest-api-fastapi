from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field, SQLModel
from datetime import date, datetime
import uuid

class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now()))

    def __repr__(self):
        return f"<Book {self.title}>"