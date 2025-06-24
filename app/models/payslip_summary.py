class EmployeePayslipSummary:
    def __init__(self, employee_id: int, total_take_home: float):
        self.employee_id = employee_id
        self.total_take_home = total_take_home

class PayslipSummary:
    def __init__(self, employee_summaries: list, grand_total: float):
        self.employee_summaries = employee_summaries
        self.grand_total = grand_total