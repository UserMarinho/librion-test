from fastapi import APIRouter, Depends, HTTPException, Query
from infrastructure.dependencies import get_session
from sqlalchemy.orm import Session
from services import BookService, CopyService
from schemas import BookSearch
from exceptions.book_exception import BookNotFoundError

# Roteador para operações com livros
books_router = APIRouter(prefix="/books", tags=["books"])

# Retorna todos os livros
@books_router.get("/")
async def get_books(session:Session = Depends(get_session)):
    """Get all books"""
    return BookService.list_books(session)

# Rota para filtrar livros
@books_router.post("/search")
async def filter_books(filters:BookSearch, session:Session = Depends(get_session)):
    """Search using a combination of filters."""
    return BookService.filter_books(filters, session)

# Rota para buscar um livro pelo seu Id
@books_router.get("/{book_id}")
async def get_book_by_id(book_id:int, session:Session = Depends(get_session)):
    """Get book by id"""
    try:
        return BookService.get_by_id(book_id, session)
    
    except BookNotFoundError:
        raise HTTPException(status_code=404)

# Rota para buscar as cópias registradas de um livro
@books_router.get("/{book_id}/copies")
async def get_copies(book_id:int, session:Session = Depends(get_session)):
    """Get copies of a book"""
    return CopyService.get_copies_by_book(session, book_id)