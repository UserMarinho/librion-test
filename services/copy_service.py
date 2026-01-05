from sqlalchemy.orm import Session
from infrastructure.repositories import CopyRepository, BookRepository
from models import Copy, Book
from exceptions.copy_exception import IsbnNotFoundError
from utils import search_book
from schemas import CopyCreate

class CopyService():

    @staticmethod
    def create(session: Session, data_copy:CopyCreate, library_id:int):
        book = BookRepository.find_by_isbn(session, data_copy.isbn)

        if book:
            copy = Copy(**data_copy.model_dump(exclude={"isbn"}), id_library = library_id, id_book = book.id)
            return CopyRepository.create(session, copy)
        else: 
            try:
                book_data = search_book(data_copy.isbn)
                book = Book(**book_data.model_dump())
                book = BookRepository.create(session, book)
                copy = Copy(**data_copy.model_dump(exclude={"isbn"}), id_library = library_id, id_book = book.id)
                return CopyRepository.create(session, copy)
                
            except IsbnNotFoundError as e:
                raise IsbnNotFoundError(str(e))
            
    @staticmethod
    def get_all(session: Session, id_library: int):
        all_copies = CopyRepository.get_all(session, id_library)
        return all_copies
