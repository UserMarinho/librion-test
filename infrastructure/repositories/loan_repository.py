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
    
    @staticmethod
    def list_library_loans(session:Session, library_id:id):
        query = session.query(Loan).join(Copy).filter(Copy.id_library == library_id)
        return query.all()
    
    @staticmethod
    def get_loan_by_id(session:Session, loan_id:int):
        query = session.query(Loan).filter(Loan.id == loan_id)

        return query.first()
    
    @staticmethod
    def register_taken_date(session:Session, loan_id:int):
        query = session.query(Loan).filter(Loan.id == loan_id).first()