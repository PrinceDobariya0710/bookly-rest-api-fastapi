from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, Field

from src.books.schemas import Book
from src.reviews.schemas import ReviewModel

class UserCreateModel(BaseModel):
    username: str = Field(max_length=15)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    first_name: str 
    last_name: str
    is_verified: bool
    email: str
    password_hash: str = Field(exclude=True)
    created_at: datetime 
    updated_at: datetime 

class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]

class UserLoginModel(BaseModel):
    email: str
    password: str