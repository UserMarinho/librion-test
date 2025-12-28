from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.connectionDB import Base

# classe de exemplares
class Copy(Base):
    
    __tablename__ = 'copy'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    id_library = Column('id_library', ForeignKey('library.id'))
    id_book = Column('id_book', ForeignKey('book.id'))
    quantity = Column('quantity', Integer, nullable=False)
    is_global = Column('is_global', Boolean, nullable=False)

    book = relationship('Book', back_populates='copies')
    library = relationship('Library', uselist=False)
    
    def __init__(self, id_library: int, id_book: int, quantity: int, is_global: bool):
        self.id_library = id_library
        self.id_book = id_book
        self.quantity = quantity
        self.is_global = is_global
