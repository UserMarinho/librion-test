from fastapi import APIRouter, Depends, HTTPException, Query
from infrastructure.dependencies import get_session
from sqlalchemy.orm import Session
from services import BookService
from schemas import SearchBook
from exceptions.book_exception import BookNotFoundError

books_router = APIRouter(prefix="/books", tags=["books"])

@books_router.get("/")
async def get_books(cursor:int = Query(1, ge=1), size:int = Query(10, le=50), session:Session = Depends(get_session)):
    """Get books limit by cursor and size"""
    return BookService.list_books(cursor, size, session)

@books_router.post("/search")
async def filter_books(filters:SearchBook, session:Session = Depends(get_session)):
    """Search using a combination of filters."""
    return BookService.filter_books(filters, session)

@books_router.get("/{book_id}")
async def get_book_by_id(book_id:int, session:Session = Depends(get_session)):
    """Get book by id"""
    try:
        return BookService.get_by_id(book_id, session)
    except BookNotFoundError:
        raise HTTPException(status_code=404)

@books_router.get("/{book_id}/copies")
async def get_copies(book_id:int, session:Session = Depends(get_session)):
    """Get copies of a book"""
    try:
        return BookService.get_copies(book_id, session)
    
    except BookNotFoundError:
        raise HTTPException(status_code=404)