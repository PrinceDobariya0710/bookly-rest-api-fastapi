from typing import List
from fastapi import APIRouter, HTTPException,status, Depends
from src.books.schemas import Book, BookCreateModel, BookUpdateModel
from src.books.service import BookService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

book_router = APIRouter()
book_service = BookService()

@book_router.get("/", response_model=List[Book])
async def get_all_books(session:AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED,response_model=Book)
async def create_a_book(book_data: BookCreateModel,session:AsyncSession = Depends(get_session)) -> dict:
    new_book = await book_service.create_book(book_data=book_data,session=session)
    return new_book


@book_router.get("/{book_id}")
async def get_book(book_uid: int,session:AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid=book_uid,session=session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch("/{book_id}")
async def update_book(book_uid: int,book_update_data:BookUpdateModel,session:AsyncSession = Depends(get_session)) -> dict:
    updated_book = await book_service.update_book(book_uid=book_uid,update_data=book_update_data,session=session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/{book_uid}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: int,session:AsyncSession = Depends(get_session)):
    delete_book = await book_service.delete_book(book_uid=book_uid,session=session)
    if delete_book:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")