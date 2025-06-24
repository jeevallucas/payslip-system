from datetime import date

class AttendanceDetail:
    def __init__(self, date: date):
        self.date = date

class OvertimeDetail:
    def __init__(self, date: date, hours: float):
        self.date = date
        self.hours = hours

class ReimbursementDetail:
    def __init__(self, id: int, amount: float, description: str, created_at: date):
        self.id = id
        self.amount = amount
        self.description = description
        self.created_at = created_at