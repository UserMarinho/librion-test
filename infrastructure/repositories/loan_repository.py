from sqlalchemy.orm import Session
from models import Copy, Loan

class LoanRepository:

    @staticmethod
    def register_loan(session: Session, loan: Loan):
        session.add(loan)
        session.commit()
        session.refresh(loan)

        return loan
    
    @staticmethod
    def list_reader_loans(session:Session, reader_id:int):
        query = session.query(Loan).filter(Loan.reader_id == reader_id)
        
        return query.all()