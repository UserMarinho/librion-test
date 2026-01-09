from sqlalchemy.orm import Session
from main import bcrypt_context
from infrastructure.repositories import ReaderRepository
from models import Reader
from schemas import ReaderCreate
from exceptions.reader_exception import ReaderAlreadyExistsError, ReaderNotFoundError

class ReaderService():
    # método para criar um novo leitor
    @staticmethod
    def create(session:Session, reader_data:ReaderCreate, library_id:int):
        reader = ReaderRepository.find_by_email(session, reader_data.email)

        if reader:
            raise ReaderAlreadyExistsError('Já existe um usuário cadastrado com esse email')
        
        # cria senha criptografada
        reader_data.password = bcrypt_context.hash(reader_data.password)
        
        # objeto já com a senha criptografada
        reader = Reader(**reader_data.model_dump(), id_library=library_id)

        # cria um novo leitor
        return ReaderRepository.create(session, reader)

    @staticmethod
    def list_readers_by_library(session: Session, id_library: int):
        readers = ReaderRepository.list_readers_by_library(session, id_library)

        if not readers:
            return []

        return readers
    
    @staticmethod
    def find_reader(session: Session, reader_id: int):
         # Busca o leitor no banco de dados
        reader = ReaderRepository.find_reader_by_id(session, reader_id)

        # Erro: O leitor não foi encontrado
        if not reader:
            raise ReaderNotFoundError(str("Leitor não encontrado!"))
        
        return reader