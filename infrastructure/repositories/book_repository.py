from sqlalchemy.orm import Session, Query, joinedload
from sqlalchemy import exists
from models import Book, Copy, Library
from schemas import SearchBook
from utils import normalize_string

# repositório de um livro
class BookRepository():
    
    @staticmethod
    def create(session: Session, book: Book):
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

    @staticmethod
    def find_by_isbn(session: Session, isbn: str):
        book = session.query(Book).filter(Book.isbn == isbn).first()
        return book
    
    @staticmethod
    def get_by_id(id:int, session:Session):
        return session.query(Book).where(Book.id == id).first()
    
    @staticmethod
    def list_books(cursor:int|None, size:int, session:Session):
        query = session.query(Book)

        if cursor:
            query = query.filter(Book.id > cursor)
        
        books = query.limit(size).all()

        return books

    def __filter_by_title(query:Query[Book], title:str|None):
        if not title or title == "":
            return query
        
        return query.where(Book.search_title.contains(title))
        
    def __filter_by_categories(query:Query[Book], category_ids:list[int]|None):
        if not category_ids:
            return query
        
        return query.where(Book.id_category.in_(category_ids))
    
    def __filter_by_libraries(query:Query[Book], library_ids:list[int]|None):
        if not library_ids:
            return query

        return query.where(Copy.id_library.in_(library_ids))
    
    def __availables(query:Query[Book]):
        return query.where(
            exists().where(
                (Copy.id_library == Book.id) &
                (Copy.quantity > 0)
            )
        )
    
    @staticmethod
    def combined_filters(filters:SearchBook, session:Session):
        query = session.query(Book)
        
        if filters.title:
            query = BookRepository.__filter_by_title(query, normalize_string(filters.title))
        
        if filters.category_ids:
            query = BookRepository.__filter_by_categories(query, filters.category_ids)

        if filters.available:
            query = BookRepository.__availables(query)
        
        if filters.library_ids:
            query = query.join(Copy)
            query = BookRepository.__filter_by_libraries(query, filters.library_ids)

        return query.all()

    @staticmethod
    def list_copies(book_id:int, session:Session):
        query = (
            session.query(Copy)
            .options(joinedload(Copy.library))
            .filter(Copy.id_book == book_id)
        )
        
        return query.all()