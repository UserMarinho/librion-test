from fastapi import APIRouter, Depends, HTTPException
from infrastructure.dependencies import get_session
from sqlalchemy.orm import Session
from models import Reader
from services import ReaderService, CopyService
from schemas import CopySchema, ReaderCreate, ReaderResponse
from exceptions.reader_exception import ReaderAlreadyExistsError
from exceptions.copy_exception import IsbnNotFoundError

libraries_router = APIRouter(prefix='/libraries', tags=['libraries'])

@libraries_router.post('/{library_id}/readers', response_model=ReaderResponse, status_code=201)
async def create_reader(library_id:int, reader_data: ReaderCreate, session: Session = Depends(get_session)):
    """Cria um novo leitor na plataforma associado à uma biblioteca"""
    try:
        return ReaderService.create(session, reader_data, library_id)

    except ReaderAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

@libraries_router.get('/readers')
async def get_all_readers(library_id: int, session: Session = Depends(get_session)):
    try:
        all_readers = ReaderService.get_all(session, library_id)
        return all_readers
    
    except Exception:
        raise HTTPException(status_code=500)

@libraries_router.post('/copies')
async def create_copy(copy_schema: CopySchema, session: Session = Depends(get_session)):
    try:
        CopyService.create(session, copy_schema.id_library, copy_schema.isbn, copy_schema.quantity, copy_schema.is_global)

    except IsbnNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

@libraries_router.get('/copies')
async def get_all_copies(library_id: int, session: Session = Depends(get_session)):
    try:
        all_copies = CopyService.get_all(session, library_id)
        return all_copies
    
    except Exception:
        raise HTTPException(status_code=500)

@libraries_router.patch('copies/{id}')
async def get_copy(library_id:int, session:Session = Depends(get_session)):
    return