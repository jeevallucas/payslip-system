from pydantic import BaseModel
from datetime import date

class PayrollPeriodSchema(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    created_at: str
    updated_at: str
    created_by: int

    class Config:
        orm_mode = True