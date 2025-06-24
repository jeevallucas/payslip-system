from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReimbursementSchema(BaseModel):
    id: int
    employee_id: int
    amount: float
    description: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True