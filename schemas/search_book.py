from pydantic import BaseModel

class SearchBook(BaseModel):
    title:str|None = None
    category_ids:list[int]|None = None
    library_ids:list[int]|None = None
    available:bool|None = None