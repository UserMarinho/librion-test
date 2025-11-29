from sqlalchemy import Column, Integer, String, Boolean
from infrastructure.connectionDB import Base
from models import User

# classe de bibliotecas
class Library(User, Base):
    
    __tablename__ = 'library'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    cep = Column('cep', String, nullable=False)
    admin = Column('admin', Boolean, default=False, nullable=False)

    def __init__(self, name: str, cep: str):
        User.__init__(name, cep)
        self.admin = True
