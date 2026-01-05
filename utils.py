import requests, re, unicodedata
from exceptions.copy_exception import IsbnNotFoundError
from fastapi import HTTPException
from schemas import BookSchema

# Função genêrica para consumir de uma API externa
def get_from_api(base_url:str, params:str|dict|None):
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

# Buscar livro em API externa
def search_book(isbn:str) -> BookSchema:
    url = "https://www.googleapis.com/books/v1/volumes"
    query_isbn = "q=isbn:" + isbn 
    volumes = get_from_api(url, params=query_isbn)

    if volumes["totalItems"] == 0:
        raise IsbnNotFoundError('ISBN não encontrado ou inválido!')
    
    book = volumes["items"][0]

    return BookSchema.from_api(isbn, book)

# Função para normalizar strings
def normalize_string(text:str) -> str:

    # Retorne uma string vazia para NONE e FALSE
    if not text:
        return ""

    # Separa o acento da letra. Ex: á -> a + ´
    text = unicodedata.normalize("NFD", text)

    # Percorre o texto em loop e junta apenas:
    # caracteres com a categoria diferente de "Mn" Mark, Nonspacing (acentos, aspas...)
    # e que sejam alfanuméricos (isalnum)
    text = ''.join(c for c in text if unicodedata.category(c) != "Mn" and c.isalnum())

    return text.lower()