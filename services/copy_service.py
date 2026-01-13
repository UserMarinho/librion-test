from sqlalchemy.orm import Session
from infrastructure.repositories import CopyRepository, BookRepository
from models import Copy, Book
from exceptions.copy_exception import IsbnNotFoundError, CopyNotFoundError, CopyOutOfStock
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
    
    @staticmethod
    def find_copy(session: Session, copy_id:int):
         # Busca o exemplar no banco de dados
        copy = CopyRepository.find_copy(session, copy_id)

        # Erro: O exemplar não foi encontrado
        if not copy:
            raise CopyNotFoundError(str("Exemplar não encontrado!"))
        
        return copy

    # Retorna todas as cópias de um livro
    @staticmethod
    def get_copies_by_book(session: Session, book_id:int):
        return CopyRepository.find_by_book_id(session, book_id)
    
    # Diminui um na quantidade de cópias disponíveis para empréstimo
    @staticmethod
    def decrease_available(session: Session, copy: Copy):
        if copy.quantity_available == 0:
            raise CopyOutOfStock(str("Exemplar sem estoque para empréstimo!"))
        
        copy.quantity_available -= 1
        session.add(copy)
