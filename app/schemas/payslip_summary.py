from pydantic import BaseModel
from typing import List

class EmployeePayslipSummarySchema(BaseModel):
    employee_id: int
    total_take_home: float

class PayslipSummarySchema(BaseModel):
    employee_summaries: List[EmployeePayslipSummarySchema]
    grand_total: float