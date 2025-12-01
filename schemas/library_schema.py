from pydantic import BaseModel

class LibrarySchema(BaseModel):
    name: str
    email: str
    password: str
    cep: str
    
    class Config:
        from_attributes = True