from pydantic import BaseModel
from schemas import CopyResponse
from datetime import datetime

class LoanRequest(BaseModel):
    copy_id:int

class LoanResponse(BaseModel):
    id: int
    reader_id: int
    copy_id: int
    copy_data: CopyResponse
    request_date: datetime
    taken_date: datetime | None
    return_date: datetime
    active: bool

    