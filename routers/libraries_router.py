from fastapi import APIRouter, Depends, HTTPException
from infrastructure.dependencies import get_session, get_current_library
from sqlalchemy.orm import Session
from models import Library
from services import ReaderService, CopyService, LibraryService, LoanService
from schemas import CopyCreate, CopyResponse, ReaderCreate, ReaderResponse, ReaderUpdate,LibraryResponse
from exceptions.reader_exception import ReaderAlreadyExistsError, ReaderNotFoundError
from exceptions.copy_exception import IsbnNotFoundError, CopyAlreadyExistsError, CopyNotFoundError
from exceptions.login_exception import AccessDeniedError
from exceptions.loan_exception import LoanNotFound
from exceptions.library_exception import LibraryNotFoundError

libraries_router = APIRouter(prefix='/libraries', tags=['Libraries'])

# Obtém a lista de bibliotecas cadastradas
@libraries_router.get("/", response_model=list[LibraryResponse])
async def list_libraries(session: Session = Depends(get_session)):
    try:
        return LibraryService.get_all(session)
    
    except Exception:
        raise HTTPException(status_code=500)
    
# Obtém perfil de biblioteca autenticada
@libraries_router.get("/me")
async def get_auth_library(library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    try:
        return LibraryService.get_library_by_id(session, library.id)
    
    except LibraryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except AccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)
    
#<------------------Leitores--------------------->

# Cadastra um leitor associado a uma biblioteca
@libraries_router.post('/me/readers', response_model=ReaderResponse, status_code=201)
async def create_reader(reader_data: ReaderCreate, library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    """Cadastra um novo leitor no sistema"""
    try:
        return ReaderService.create(session, reader_data, library.id)

    except ReaderAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

# Lista os leitores de uma biblioteca
@libraries_router.get('/me/readers', response_model=list[ReaderResponse])
async def get_readers_by_library(library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    """Lista todos os leitores cadastrados por uma biblioteca"""
    try:
        return ReaderService.list_readers_by_library(session, library.id)
    
    except Exception:
        raise HTTPException(status_code=500)

# Obtém um leitor pelo id
@libraries_router.get('/me/readers/{reader_id}', response_model=ReaderResponse)
async def get_reader_by_id(reader_id: int, library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    try:
        reader = ReaderService.find_reader_in_library(session, reader_id, library.id)

        return reader

    except ReaderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except AccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

# Edita um leitor
@libraries_router.patch("/me/readers/{reader_id}", response_model=ReaderResponse)
async def patch_reader(reader_id: int, reader_data: ReaderUpdate, library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    try:
        reader = ReaderService.update(session, reader_id, reader_data, library.id)
        return reader

    except ReaderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except AccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

@libraries_router.delete("/me/readers/{reader_id}")
async def delete_reader(reader_id: int, library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    try:
        ReaderService.delete(session, reader_id, library.id)

        return True

    except ReaderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except AccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

# <------------------Cópias--------------------->

# Cadastra o exemplar de um livro na biblioteca
@libraries_router.post("/me/copies", response_model=CopyResponse)
async def create_copy(new_copy: CopyCreate, library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    """Cadastra o exemplar de um livro em uma biblioteca"""
    try:
        return CopyService.create(session, new_copy, library.id)

    except CopyAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except IsbnNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
    except Exception:
        raise HTTPException(status_code=500)

# Lista os exemplares de uma biblioteca
@libraries_router.get("/me/copies")
async def get_all_copies(library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    try:
        all_copies = CopyService.get_all(session, library.id)
        return all_copies
    
    except Exception:
        raise HTTPException(status_code=500)

# Obter um exemplar pelo id
@libraries_router.get("/me/copies/{copy_id}")
async def get_copy_by_id(copy_id: int, library: Library = Depends(get_current_library), session: Session = Depends(get_session)):
    try:
        copy = CopyService.find_copy_in_library(session, copy_id, library.id)
        return copy
    except AccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    except CopyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))

# <------------------Empréstimos--------------------->

# Retornar todos os emprëstimos de uma biblioteca
@libraries_router.get("/me/loans")
async def get_all_loans(library:Library = Depends(get_current_library), session: Session = Depends(get_session)):
    try:
        return LoanService.list_library_loans(library.id, session)
    
    except LibraryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except AccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

# Retornar um empréstimo registrado na biblioteca
@libraries_router.get("/me/loans/{loan_id}")
async def get_loan_by_id(loan_id:int, library:Library = Depends(get_current_library), session: Session = Depends(get_session)):
    try:
        return LoanService.get_library_loan(library.id, loan_id, session)
    
    except LoanNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except AccessDeniedError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

# Registrar a data em que foi retirado o livro
@libraries_router.patch("/me/loans/{id_loan}/register-taken-date")
async def register_taken_date():
    pass

# Registrar a data de devolução
@libraries_router.patch("/me/loans/{id_loan}/register-return-date")
async def register_return_date():
    pass