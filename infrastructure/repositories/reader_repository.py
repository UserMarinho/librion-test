from sqlalchemy.orm import Session
from models import Reader

# repositório de leitores
class ReaderRepository():

    @staticmethod
    def create(session: Session, reader: Reader):
        session.add(reader)
        session.commit()
        return reader
    
    @staticmethod
    def list_readers_by_library(session: Session, id_library: int):
        all_readers = session.query(Reader).filter(Reader.id_library == id_library).all()
        return all_readers

    @staticmethod
    def find_by_email(session: Session, email: str):
        reader = session.query(Reader).filter(Reader.email == email).first()
        return reader
