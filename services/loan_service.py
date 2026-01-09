from sqlalchemy.orm import Session
from models import Loan
from schemas import LoanRequest
from services import ReaderService, CopyService
from exceptions.copy_exception import CopyOutOfStock
from exceptions.loan_exception import LoanDenied
from infrastructure.repositories import LoanRepository

class LoanService():
    
    @staticmethod
    def request_loan(data_request: LoanRequest, session: Session):
        # Busca o exemplar no banco de dados
        copy = CopyService.find_copy(session, data_request.copy_id)

        # Erro: Não há exemplar disponível
        if copy.quantity_available == 0:
            raise CopyOutOfStock(str("Sem estoque disponível para empréstimo!"))
        
        # Busca o leitor no banco de dados
        reader = ReaderService.find_reader(session, data_request.reader_id)
        
        # Erro: O livro não é global e não pertence a biblioteca de origem do leitor
        if not copy.is_global and copy.id_library != reader.id_library:
            raise LoanDenied(str("O usuário não tem permissão de solicitar o empréstimo desse exemplar"))
        
        # Diminui um na quantidade de exemplares disponíveis
        CopyService.decrease_available(session, copy)
        
        loan = Loan(**data_request.model_dump())
        LoanRepository.register_loan(session, loan)
        
        return loan