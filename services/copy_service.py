from sqlalchemy.orm import Session
from infrastructure.repositories import CopyRepository, BookRepository
from models import Copy, Book
from exceptions.copy_exception import IsbnNotFoundError
from utils import search_book

class CopyService():

    @staticmethod
    def create(session: Session, id_library: int, isbn: str, quantity: int, is_global: bool):
        book = BookRepository.find_by_isbn(session, isbn)

        if book:
            copy = Copy(id_library, book.id, quantity, is_global)
            CopyRepository.create(session, copy)
        else: 
            try:
                book_data = search_book(isbn)
                book = Book(**book_data.model_dump())
                book = BookRepository.create(session, book)
                copy = Copy(id_library, book.id, quantity, is_global)
                CopyRepository.create(session, copy)
                
            except IsbnNotFoundError as e:
                raise IsbnNotFoundError(str(e))
            
    @staticmethod
    def get_all(session: Session, id_library: int):
        all_copies = CopyRepository.get_all(session, id_library)
        return all_copies
