from pydantic import BaseModel
from typing import List
from datetime import date

# Nested Schemas
class AttendanceDetailSchema(BaseModel):
    date: date

class OvertimeDetailSchema(BaseModel):
    date: date
    hours: float

class ReimbursementDetailSchema(BaseModel):
    id: int
    amount: float
    description: str
    created_at: str

# Main Payslip Schema
class PayslipDetailSchema(BaseModel):
    employee_id: int
    base_salary: float
    attendance_days: int
    attendance_details: List[AttendanceDetailSchema]
    overtime_hours: float
    overtime_amount: float
    overtime_details: List[OvertimeDetailSchema]
    reimbursements: List[ReimbursementDetailSchema]
    reimbursement_total: float
    total: float

    class Config:
        orm_mode = True