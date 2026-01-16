from sqlalchemy.orm import Session, Query
from models import Book, Copy
from schemas import BookSearch
from utils import normalize_string

class BookRepository():
    
    # Criar um novo livro
    @staticmethod
    def create(session: Session, book: Book):
        session.add(book)
        session.commit()
        session.refresh(book)
        return book
    
    # Encontrar um livro por o seu isbn
    @staticmethod
    def find_by_isbn(session: Session, isbn: str):
        book = session.query(Book).filter(Book.isbn == isbn).first()
        return book
    
    # Encontrar um livro por o seu id
    @staticmethod
    def find_by_id(id:int, session:Session):
        return session.query(Book).where(Book.id == id).first()
    
    # Retornar todos os livros
    @staticmethod
    def list_books(session:Session):
        query = session.query(Book)
        return query.all()

    # Função privada para combinar query de filtro
    # Obs: Retorna uma Query, não um item do banco
    def __filter_by_title(query:Query[Book], title:str|None):
        if not title or title == "":
            return query
        
        return query.where(Book.search_title.contains(title))

    #Função privada para combinar query de filtro
    # Obs: Retorna uma Query, não um item do banco    
    def __filter_by_categories(query:Query[Book], category_ids:list[int]|None):
        if not category_ids:
            return query
        
        return query.where(Book.id_category.in_(category_ids))
    
    #Função privada para combinar query de filtro
    # Obs: Retorna uma Query, não um item do banco 
    def __filter_by_libraries(query:Query[Book], library_ids:list[int]|None):
        if not library_ids:
            return query

        return query.where(Copy.id_library.in_(library_ids))
    
    #Função privada para combinar query de filtro
    # Obs: Retorna uma Query, não um item do banco 
    def __availables(query:Query[Book]):
        return query.filter(Book.copies.any(Copy.quantity_available > 0))
    
    # Combina os filtros
    @staticmethod
    def combined_filters(filters:BookSearch, session:Session):
        query = session.query(Book)
        
        if filters.title:
            query = BookRepository.__filter_by_title(query, normalize_string(filters.title))
        
        if filters.category_ids:
            query = BookRepository.__filter_by_categories(query, filters.category_ids)

        if filters.available:
            query = BookRepository.__availables(query)
        
        if filters.library_ids:
            query = query.join(Copy)
            query = BookRepository.__filter_by_libraries(query, filters.library_ids)

        return query.all()
