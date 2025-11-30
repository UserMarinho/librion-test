from sqlalchemy import Column, Integer, String
from infrastructure.connectionDB import Base

# classe de categorias
class Category(Base):
    
    __tablename__ = 'category'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

