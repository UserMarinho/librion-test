from sqlalchemy.orm import Session
from infrastructure.repositories import LibraryRepository as r
from models import Library
from exceptions.library_exception import LibraryAlreadyExistsError

class LibraryService():

    @staticmethod
    def create(session: Session, new_library: Library):
        library = r.find_by_email(session, new_library.email)

        if library:
            raise LibraryAlreadyExistsError("Já existe uma biblioteca registrada com esse email!")
        r.create(session, new_library)
