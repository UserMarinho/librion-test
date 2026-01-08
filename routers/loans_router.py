from fastapi import APIRouter, Depends, HTTPException
from infrastructure.dependencies import get_session
from sqlalchemy.orm import Session
from schemas import LoanRequest
from services import LoanService
from exceptions.loan_exception import LoanDenied
from exceptions.copy_exception import CopyOutOfStock, CopyNotFoundError
from exceptions.reader_exception import ReaderNotFoundError

loans_router = APIRouter(prefix="/loans", tags=["Loan"])

# (LEITOR) - Solicitação de empréstimo
@loans_router.post("/")
async def request_loan(data_request:LoanRequest, session:Session = Depends(get_session)):
    try:
        return LoanService.request_loan(data_request, session)
    
    except CopyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except CopyOutOfStock as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    except ReaderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except LoanDenied as e:
        raise HTTPException(status_code=403, detail=str(e))

# (LEITOR E ADM) - Lista de empréstimos [todos, atrasados, pendentes, concluídos]
@loans_router.get("/")
async def list_loans(session: Session = Depends(get_session)):
    pass

# (LEITOR E ADM) - Visualizar empréstimo
@loans_router.get("/{id_loan}")
async def get_loan_by_id(session: Session = Depends(get_session)):
    pass

# (ADM) - Registra a data em que foi retirado o livro
@loans_router.patch("/{id_loan}/register-taken-date")
async def register_taken_date():
    pass

# (ADM) - Registra a data de devolução
@loans_router.patch("/{id_loan}/register-return-date")
async def register_return_date():
    pass