from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.connectionDB import Base
from utils import normalize_string

# classe de livros
class Book(Base):

    __tablename__ = 'book'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    id_category = Column('id_category', ForeignKey('category.id'))
    title = Column('title', String, nullable=False)
    author = Column('author', String, nullable=False)
    description = Column('description', String)
    image = Column('image', String, nullable=False)
    age_rating = Column('age_rating', String, nullable=False)
    isbn =  Column('isbn', String, unique=True, nullable=False)
    search_title = Column('search_title', String, nullable=False)

    copies = relationship('Copy', back_populates='book')
    
    def __init__(self, id_category: int, title: str, author: str, description: str, image: str, age_rating: str, isbn: str):
        self.id_category = id_category
        self.title = title
        self.search_title = normalize_string(title)
        self.author = author
        self.description = description
        self.image = image
        self.age_rating = age_rating
        self.isbn = isbn
