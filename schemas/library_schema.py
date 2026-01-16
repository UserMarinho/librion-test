from pydantic import BaseModel

class LibraryCreate(BaseModel):
    name: str
    email: str
    password: str
    cep: str
    
    class Config:
        from_attributes = True

class LibraryResponse(BaseModel):
    name: str
    cep: str

    class Config:
        from_attributes = True
    