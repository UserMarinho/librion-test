from pydantic import BaseModel

class ReaderBase(BaseModel):
    name:str
    email:str
    cep:str

    class Config:
        from_attributes = True

class ReaderCreate(ReaderBase):
    password:str

    class Config:
        from_attributes = True


class ReaderResponse(ReaderBase):
    id_library: int

    class Config:
        from_attributes = True
