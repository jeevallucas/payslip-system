from typing import List
from app.models.payslip_detail import AttendanceDetail, OvertimeDetail, ReimbursementDetail

class PayslipDetail:
    def __init__(
        self,
        employee_id: int,
        base_salary: float,
        attendance_days: int,
        attendance_details: List[AttendanceDetail],
        overtime_hours: float,
        overtime_amount: float,
        overtime_details: List[OvertimeDetail],
        reimbursements: List[ReimbursementDetail],
        reimbursement_total: float,
        total: float
    ):
        self.employee_id = employee_id
        self.base_salary = base_salary
        self.attendance_days = attendance_days
        self.attendance_details = attendance_details
        self.overtime_hours = overtime_hours
        self.overtime_amount = overtime_amount
        self.overtime_details = overtime_details
        self.reimbursements = reimbursements
        self.reimbursement_total = reimbursement_total
        self.total = total