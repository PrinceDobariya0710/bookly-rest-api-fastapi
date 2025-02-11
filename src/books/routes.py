from typing import List
from fastapi import APIRouter, HTTPException,status, Depends
from src.books.schemas import Book, BookCreateModel, BookUpdateModel, BookDetail
from src.books.service import BookService
from src.constants import ALLOWED_ROLES
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(allowed_roles=ALLOWED_ROLES))

@book_router.get("/", response_model=List[Book],dependencies=[role_checker])
async def get_all_books(session:AsyncSession = Depends(get_session),token_details:dict=Depends(access_token_bearer)):
    books = await book_service.get_all_books(session)
    return books

@book_router.get("/user/{user_uid}", response_model=List[Book],dependencies=[role_checker])
async def get_user_books_submissions(user_uid:str ,session:AsyncSession = Depends(get_session),token_details:dict=Depends(access_token_bearer)):
    books = await book_service.get_user_books(user_uid,session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED,response_model=Book,dependencies=[role_checker])
async def create_a_book(book_data: BookCreateModel,session:AsyncSession = Depends(get_session),token_details:dict=Depends(access_token_bearer)) -> dict:
    user_uid = token_details.get('user')['user_uid']
    new_book = await book_service.create_book(book_data=book_data,user_uid=user_uid,session=session)
    return new_book


@book_router.get("/{book_uid}",response_model=BookDetail,dependencies=[role_checker])
async def get_book(book_uid: str,session:AsyncSession = Depends(get_session),token_details:dict=Depends(access_token_bearer)) -> dict:
    book = await book_service.get_book(book_uid=book_uid,session=session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch("/{book_uid}",response_model=Book,dependencies=[role_checker])
async def update_book(book_uid: str,book_update_data:BookUpdateModel,session:AsyncSession = Depends(get_session),token_details:dict=Depends(access_token_bearer)) -> dict:
    updated_book = await book_service.update_book(book_uid=book_uid,update_data=book_update_data,session=session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/{book_uid}",status_code=status.HTTP_204_NO_CONTENT,dependencies=[role_checker])
async def delete_book(book_uid: str,session:AsyncSession = Depends(get_session),token_details:dict=Depends(access_token_bearer)):
    delete_book = await book_service.delete_book(book_uid=book_uid,session=session)
    if delete_book:
        return {"detail":f"{book_uid} is deleted."}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")