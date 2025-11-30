from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from infrastructure.connectionDB import Base
from .user import User

# classe de leitores
class Reader(User, Base):
    
    __tablename__ = 'reader'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    id_library = Column('id_library', ForeignKey('library.id'))
    name = Column('name', String, nullable=False)
    email = Column('email', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    cep = Column('cep', String, nullable=False)
    admin = Column('admin', Boolean, default=False, nullable=False)

    def __init__(self, id_library: int ,name: str, email: str, password: str, cep: str):
        super().__init__(name, email, password, cep)
        self.id_library = id_library
        
