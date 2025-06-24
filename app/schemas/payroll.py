from pydantic import BaseModel
from datetime import date
from typing import Optional

class ProcessPayrollRequest(BaseModel):
    payroll_period_id: int

class PayslipResponse(BaseModel):
    id: int
    employee_id: int
    payroll_period_id: int
    base_salary: float
    attendance_days: int
    overtime_hours: float
    overtime_amount: float
    reimbursement_total: float
    total: float
    created_at: str

    class Config:
        orm_mode = True