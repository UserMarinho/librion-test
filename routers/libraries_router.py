from fastapi import APIRouter, Depends, HTTPException
from infrastructure.dependencies import get_session, get_current_library
from sqlalchemy.orm import Session
from models import Library
from services import ReaderService, CopyService
from schemas import CopyCreate, CopyResponse, ReaderCreate, ReaderResponse
from exceptions.reader_exception import ReaderAlreadyExistsError
from exceptions.copy_exception import IsbnNotFoundError

libraries_router = APIRouter(prefix='/libraries', tags=['libraries'], dependencies=[Depends(get_current_library)])

# Cadastra um leitor associado a uma biblioteca
@libraries_router.post('/readers', response_model=ReaderResponse, status_code=201)
async def create_reader(reader_data: ReaderCreate, library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    """Cadastra um novo leitor no sistema"""
    try:
        return ReaderService.create(session, reader_data, library.id)

    except ReaderAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

# Obtém um leitor pelo id
@libraries_router.get('/{library_id}/readers/{reader_id}')
async def get_reader_by_id():
    pass

# Lista os leitores de uma biblioteca
@libraries_router.get('/readers', response_model=list[ReaderResponse])
async def get_readers_by_library(library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    """Lista todos os leitores cadastrados por uma biblioteca"""
    try:
        return ReaderService.list_readers_by_library(session, library.id)
    
    except Exception:
        raise HTTPException(status_code=500)

# Edita um leitor
@libraries_router.patch("/{library_id}/readers/{reader_id}")
async def patch_reader():
    pass

# Cadastra o exemplar de um livro na biblioteca
@libraries_router.post('/copies', response_model=CopyResponse)
async def create_copy(new_copy: CopyCreate, library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    """Cadastra o exemplar de um livro em uma biblioteca"""
    try:
        return CopyService.create(session, new_copy, library.id)

    except IsbnNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

# Obter um exemplar pelo id
@libraries_router.get("/{library_id}/copies/{copy_id}")
async def get_copy_by_id():
    pass

# Lista os exemplares de uma biblioteca
@libraries_router.get('copies/')
async def get_all_copies(library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    try:
        all_copies = CopyService.get_all(session, library.id)
        return all_copies
    
    except Exception:
        raise HTTPException(status_code=500)