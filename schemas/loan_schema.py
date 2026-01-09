from pydantic import BaseModel

class LoanRequest(BaseModel):
    copy_id:int
    reader_id:int