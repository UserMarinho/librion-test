from sqlalchemy.orm import Session
from models import Reader
from main import bcrypt_context
from schemas import ReaderUpdate

# repositório de leitores
class ReaderRepository():

    @staticmethod
    def find_reader_by_id(session: Session, id_reader:int):
        query = session.query(Reader).filter(Reader.id == id_reader).first()
        return query

    @staticmethod
    def create(session: Session, reader: Reader):
        # cria senha criptografada
        reader.password = bcrypt_context.hash(reader.password)

        session.add(reader)
        session.commit()
        return reader
    
    @staticmethod
    def update(session: Session, reader: Reader, data: ReaderUpdate):
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(reader, field, value)

        session.commit()
        session.refresh(reader)

        return reader
        

    @staticmethod
    def delete(session: Session, reader: Reader):
        session.delete(reader)
        session.commit()


    @staticmethod
    def list_readers_by_library(session: Session, id_library: int):
        all_readers = session.query(Reader).filter(Reader.id_library == id_library).all()
        return all_readers

    @staticmethod
    def find_by_email(session: Session, email: str):
        reader = session.query(Reader).filter(Reader.email == email).first()
        return reader
