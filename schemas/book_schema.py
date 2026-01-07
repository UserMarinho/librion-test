from pydantic import BaseModel

class BookSchema(BaseModel):
    id_category:int|None = None
    title:str
    author:str
    description:str
    image:str
    age_rating:str
    isbn:str

    @classmethod
    def from_api(cls, isbn, data:dict):
        info = data.get("volumeInfo", {})
        image_links = info.get("imageLinks", {})
        default = "(vazio)"

        return cls(
            author = info.get("authors", default)[0],
            description = info.get("description", default),
            title = info.get("title", default),
            isbn = isbn,
            age_rating = info.get("maturityRating", None),
            image = image_links.get("thumbnail") or image_links.get("smallThumbnail") or default,
        )

    class Config:
        from_attributes = True

class BookSearch(BaseModel):
    title:str|None = None
    category_ids:list[int]|None = None
    library_ids:list[int]|None = None
    available:bool|None = None