from fastapi import APIRouter, Depends, HTTPException
from infrastructure.dependencies import get_session, get_current_reader
from sqlalchemy.orm import Session
from models import Reader
from services import LoanService
from schemas import LoanRequest, LoanResponse
from exceptions.loan_exception import LoanDenied, LoanNotFound
from exceptions.copy_exception import CopyOutOfStock, CopyNotFoundError
from exceptions.reader_exception import ReaderNotFoundError
from exceptions.login_exception import AccessDeniedError

readers_router = APIRouter(prefix="/readers", tags=["Readers"])

# Retornar dados do leitor 
@readers_router.get("/me")
async def get_profile():
    pass

# Listar todos os empréstimos de um leitor
@readers_router.get("/me/loans", response_model=list[LoanResponse])
async def list_reader_loans(reader: Reader = Depends(get_current_reader), session: Session = Depends(get_session)):
    """Lista de todos os empréstimos de um leitor"""
    try:
        return LoanService.list_reader_loans(reader.id, session)
    
    except ReaderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sollicitar um empréstimo
@readers_router.post("/me/loans")
async def request_loan(loan_request: LoanRequest, reader:Reader = Depends(get_current_reader), session:Session = Depends(get_session)):
    """Solicitar o empréstimo de um exemplar (cópia)"""
    try:
        return LoanService.request_loan(loan_request.copy_id, reader.id, session)
    
    except CopyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except CopyOutOfStock as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    except ReaderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except LoanDenied as e:
        raise HTTPException(status_code=403, detail=str(e))

# Visualizar empréstimo
@readers_router.get("/me/loans/{loan_id}")
async def get_loan_by_id(loan_id:int, reader:Reader = Depends(get_current_reader), session: Session = Depends(get_session)):
    try:
        return LoanService.get_reader_loan(reader.id, loan_id, session)
    
    except LoanNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except AccessDeniedError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

@readers_router.patch("/me/loans/{loan_id}/renew")
async def renew_loan():
    pass
