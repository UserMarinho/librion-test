from pydantic import BaseModel

class CopyBase(BaseModel):
    quantity: int
    is_global: bool

    class Config:
        from_attributes = True
    
class CopyCreate(CopyBase):
    isbn: str

    class Config:
        from_attributes = True

class CopyResponse(CopyBase):
    id_library:int
    id_book:int
    
    class Config:
        from_attributes = True