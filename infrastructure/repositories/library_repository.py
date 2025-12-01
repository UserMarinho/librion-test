from sqlalchemy.orm import Session
from models import Library

# repositório de biblioteca
class LibraryRepository():

    @staticmethod
    def create(session: Session, library: Library):
        session.add(library)
        session.commit()

    @staticmethod
    def find_by_email(session: Session, email: str):
        library = session.query(Library).filter(Library.email == email).first()
        return library
    