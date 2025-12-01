from fastapi import APIRouter, Depends, HTTPException
from infrastructure.dependencies import get_session
from main import bcrypt_context
from sqlalchemy.orm import Session
from models import Library
from services import LibraryService
from schemas import LibrarySchema
from exceptions.library_exception import LibraryAlreadyExistsError

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.post('/create_library')
async def create_library(library_schema: LibrarySchema, session: Session = Depends(get_session)):
    try:
        # cria senha criptografada
        crypt_password = bcrypt_context.hash(library_schema.password)

        # cria uma nova biblioteca no banco de dados
        library = Library(library_schema.name, library_schema.email, crypt_password, library_schema.cep)
        LibraryService.create(session, library)

    except LibraryAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)
    