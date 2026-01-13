from fastapi import APIRouter, Depends, HTTPException
from infrastructure.dependencies import get_session, get_current_reader, get_current_library
from sqlalchemy.orm import Session
from models import Reader, Library
from services import LoanService
from exceptions.loan_exception import LoanDenied
from exceptions.copy_exception import CopyOutOfStock, CopyNotFoundError
from exceptions.reader_exception import ReaderNotFoundError

loans_router = APIRouter(prefix="/loans", tags=["Loan"])

# (BIBLIOTECA) - Lista de empréstimos de uma biblioteca
@loans_router.get("/")
async def list_library_loans(library:Library = Depends(get_current_library), session: Session = Depends(get_session)):
    """Lista de todos os empréstimos de uma biblioteca"""
    pass

# (LEITOR) - Lista de empréstimos de um leitor
@loans_router.get("/me")
async def list_reader_loans(reader: Reader = Depends(get_current_reader), session: Session = Depends(get_session)):
    """Lista de todos os empréstimos de um leitor"""
    try:
        return LoanService.list_reader_loans(reader.id, session)
    
    except ReaderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# (LEITOR) - Solicitação de empréstimo
@loans_router.post("/")
async def request_loan(copy_id:int, session:Session = Depends(get_session), reader:Reader = Depends(get_current_reader)):
    """Solicitar o empréstimo de um exemplar (cópia)"""
    try:
        return LoanService.request_loan(copy_id, reader.id, session)
    
    except CopyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except CopyOutOfStock as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    except ReaderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except LoanDenied as e:
        raise HTTPException(status_code=403, detail=str(e))

# (LEITOR) - Visualizar empréstimo
@loans_router.get("/{id_loan}")
async def get_loan_by_id(session: Session = Depends(get_session)):
    pass

# (BIBLIOTECA) - Registra a data em que foi retirado o livro
@loans_router.patch("/{id_loan}/register-taken-date")
async def register_taken_date():
    pass

# (BIBLIOTECA) - Registra a data de devolução
@loans_router.patch("/{id_loan}/register-return-date")
async def register_return_date():
    pass