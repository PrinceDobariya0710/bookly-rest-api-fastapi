from datetime import datetime
import uuid
from pydantic import BaseModel, Field

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

class UserLoginModel(BaseModel):
    email: str
    password: str