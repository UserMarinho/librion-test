from sqlalchemy.orm import Session
from models import Loan
from services import ReaderService, CopyService
from exceptions.copy_exception import CopyOutOfStock
from exceptions.loan_exception import LoanDenied
from infrastructure.repositories import LoanRepository

class LoanService():
    
    @staticmethod
    def request_loan(copy_id:int, reader_id:int, session:Session):
        # Busca o exemplar no banco de dados
        copy = CopyService.find_copy(session, copy_id)

        # Erro: Não há exemplar disponível
        if copy.quantity_available == 0:
            raise CopyOutOfStock(str("Sem estoque disponível para empréstimo!"))
        
        # Busca o leitor no banco de dados
        reader = ReaderService.find_reader(session, reader_id)
        
        # Erro: O livro não é global e não pertence a biblioteca de origem do leitor
        if not copy.is_global and copy.id_library != reader.id_library:
            raise LoanDenied(str("O usuário não tem permissão de solicitar o empréstimo desse exemplar"))
        
        # Diminui um na quantidade de exemplares disponíveis
        CopyService.decrease_available(session, copy)
        
        loan = Loan(copy_id, reader_id)
        LoanRepository.register_loan(session, loan)
        
        return loan
    
    @staticmethod
    def list_reader_loans(reader_id:int, session:Session):
        # Busca o leitor no banco, caso não exista, raise exception
        reader = ReaderService.find_reader(session, reader_id)
        return LoanRepository.list_reader_loans(session, reader.id)
