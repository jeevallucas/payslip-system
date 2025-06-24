from datetime import datetime

class ReimbursementCreate:
    def __init__(self, employee_id: int, amount: float, description: str = None):
        self.employee_id = employee_id
        self.amount = amount
        self.description = description