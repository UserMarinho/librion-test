from sqlalchemy.orm import Session
from infrastructure.repositories import ReaderRepository
from models import Reader
from schemas import ReaderCreate, ReaderUpdate
from exceptions.reader_exception import ReaderAlreadyExistsError, ReaderNotFoundError
from exceptions.login_exception import AccessDeniedError

class ReaderService():
    # método para criar um novo leitor
    @staticmethod
    def create(session:Session, reader_data:ReaderCreate, library_id:int):
        reader = ReaderRepository.find_by_email(session, reader_data.email)

        if reader:
            raise ReaderAlreadyExistsError('Já existe um usuário cadastrado com esse email')
        
        reader = Reader(**reader_data.model_dump(), id_library=library_id)

        # cria um novo leitor
        return ReaderRepository.create(session, reader)
    
    # atualiza as informações de um leitor no banco de dados
    @staticmethod
    def update(session:Session, reader_id: int, reader_data: ReaderUpdate, library_id: int):
        reader = ReaderService.find_reader_in_library(session, reader_id, library_id)

        reader = ReaderRepository.update(session, reader, reader_data)
        return reader
    
    @staticmethod
    def delete(session: Session, reader_id: int, library_id: int):
        reader = ReaderService.find_reader_in_library(session, reader_id, library_id)

        ReaderRepository.delete(session, reader)

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
            raise ReaderNotFoundError('Leitor não encontrado!')
        
        return reader
    
    @staticmethod
    def find_reader_in_library(session: Session, reader_id: int, library_id: int):
        # busca o leitor no banco de dados
        reader =  ReaderService.find_reader(session, reader_id)

        if reader.id_library != library_id:
            raise AccessDeniedError('Você não tem acesso a esse usuário!')
        
        return reader

    # verifica por meio do email se um Reader já está cadastrado 
    @staticmethod
    def already_registered(session: Session, email: str):
        reader = ReaderRepository.find_by_email(session, email)
        
        return reader
