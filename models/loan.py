from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from infrastructure.connectionDB import Base
from datetime import datetime, timedelta, timezone

# classe de empréstimos
class Loan(Base):
    
    __tablename__ = "loans"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    copy_id = Column('copy_id', ForeignKey("copy.id"), nullable=False)
    reader_id = Column('reader_id', ForeignKey("reader.id"), nullable=False)
    request_date = Column('request_date', DateTime, nullable=False, default=datetime.now())
    taken_date = Column('taken_date', DateTime)
    return_date = Column('return_date', DateTime)
    active = Column('active', Boolean, nullable=False)

    copy_data = relationship('Copy')

    def __init__(self, copy_id:int, reader_id:int):
        self.copy_id = copy_id
        self.reader_id = reader_id
        self.request_date = datetime.now()
        self.return_date = datetime.now() + timedelta(days=7)
        self.active = True
