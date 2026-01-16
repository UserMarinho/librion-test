from sqlalchemy.orm import Session
from infrastructure.repositories import LibraryRepository
from models import Library
from exceptions.library_exception import LibraryAlreadyExistsError, LibraryNotFoundError
from exceptions.login_exception import AccessDeniedError

class LibraryService():

    # método para criar uma nova biblioteca
    @staticmethod
    def create(session: Session, new_library: Library):
        library = LibraryRepository.find_by_email(session, new_library.email)

        if library:
            raise LibraryAlreadyExistsError('Já existe uma biblioteca registrada com esse email!')

        # cria uma nova bibliotea
        LibraryRepository.create(session, new_library)

    @staticmethod
    def get_all(session: Session):
        libraries = LibraryRepository.get_all(session)

        if not libraries:
            return []
        
        return libraries

    # verifica por meio do email se um Library já está cadastrado 
    @staticmethod
    def already_registered(session: Session, email: str):
        library = LibraryRepository.find_by_email(session, email)
        
        return library
    
    @staticmethod
    def get_library_by_id(session:Session, library_id:int):
        library = LibraryRepository.get_by_id(session, library_id)

        if not library:
            raise LibraryNotFoundError(str("Biblioteca não encontrada"))
        
        if library.id != library_id:
            raise  AccessDeniedError(str("Você não tem permissão para acessar esse recurso"))
        
        return library