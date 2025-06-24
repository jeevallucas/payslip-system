from pydantic import BaseModel
from datetime import date

class AttendanceSchema(BaseModel):
    id: int
    employee_id: int
    date: date
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True