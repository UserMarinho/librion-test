from sqlalchemy.orm import Session, joinedload
from models import Copy, Book, Library

# repositório de exemplar
class CopyRepository():
    
    @staticmethod
    def find_copy(session: Session, copy_id):
        query = session.query(Copy).filter(Copy.id == copy_id).first()
        return query
    
    # retorna um exemplar com informações do livro
    @staticmethod
    def find_copy_join_book(session: Session, copy_id):
        query = session.query(Copy).options(joinedload(Copy.book)).filter(Copy.id == copy_id).first()
        return query
    
    @staticmethod
    def find_by_isbn(session: Session, isbn: str, library_id: str):
        return (session.query(Copy).join(Book).filter(Copy.id_library == library_id, Book.isbn == isbn).first() is not None)

    @staticmethod
    def create(session: Session, copy: Copy):
        session.add(copy)
        session.commit()

        return copy

    @staticmethod
    def get_all(session: Session, id_library: int):
        all_copies = session.query(Copy).options(joinedload(Copy.book)).filter(Copy.id_library == id_library).all()
        return all_copies
    
    # Retorna todas as cópias de um livro
    @staticmethod
    def find_by_book_id(session: Session, book_id:int):
        query = session.query(Copy).options(joinedload(Copy.library)).filter(Copy.id_book == book_id)
        return query.all()