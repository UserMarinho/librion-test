from sqlalchemy.orm import Session, joinedload
from models import Copy

# repositório de exemplar
class CopyRepository():
    
    @staticmethod
    def find_copy(session: Session, copy_id):
        query = session.query(Copy).filter(Copy.id == copy_id).first()
        return query

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
        query = session.query(Copy).filter(Copy.id_book == book_id)
        return query.all()