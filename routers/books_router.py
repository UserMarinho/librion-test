from fastapi import APIRouter, Depends
from infrastructure.dependencies import get_session
from sqlalchemy.orm import Session
from services import BookService
from schemas import BookSchema, SearchBook

books_router = APIRouter(prefix="/books", tags=["books"])

@books_router.post("/search")
def get_books(filters:SearchBook, session:Session = Depends(get_session)):
    return BookService.filter_books(session, filters)

@books_router.get("/{id}")
def get_book_by_id():
    pass

@books_router.get("/{id}/copies")
def get_exemplares():
    pass