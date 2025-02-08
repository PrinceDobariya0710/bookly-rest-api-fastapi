from datetime import datetime,date
from pydantic import BaseModel
from src.reviews.schemas import ReviewModel
from typing import List
import uuid

from src.tags.schemas import TagModel

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

class BookDetail(Book):
    reviews : List[ReviewModel]
    tags:List[TagModel]