from sqlalchemy.orm import Session
from main import bcrypt_context
from models import Library

# repositório de biblioteca
class LibraryRepository():

    @staticmethod
    def create(session: Session, library: Library):
        # cria senha criptografada
        library.password = bcrypt_context.hash(library.password)

        session.add(library)
        session.commit()

    @staticmethod
    def get_all(session: Session):
        libraries = session.query(Library).all()
        return libraries

    @staticmethod
    def find_by_email(session: Session, email: str):
        library = session.query(Library).filter(Library.email == email).first()
        return library
    
    @staticmethod
    def get_by_id(session: Session, library_id:int):
        query = session.query(Library).filter(Library.id == library_id)
        return query.first()