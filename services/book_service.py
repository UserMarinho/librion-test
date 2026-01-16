from sqlalchemy.orm import Session
from infrastructure.repositories import BookRepository as r
from schemas import BookSearch
from exceptions.book_exception import BookNotFoundError

class BookService():

    @staticmethod
    def list_books(session:Session):
        books = r.list_books(session)
        return books

    @staticmethod
    def filter_books(filters:BookSearch, session:Session):
        return r.combined_filters(filters, session)
    
    @staticmethod
    def get_by_id(book_id:int, session:Session):
        book = r.find_by_id(book_id, session)

        if not book:
            raise BookNotFoundError()

        return book