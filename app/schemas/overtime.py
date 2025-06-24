from pydantic import BaseModel
from datetime import date

class OvertimeSchema(BaseModel):
    id: int
    employee_id: int
    date: date
    hours: float
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True