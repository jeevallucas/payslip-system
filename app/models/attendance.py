from datetime import date

class AttendanceCreate:
    def __init__(self, employee_id: int, date: date):
        self.employee_id = employee_id
        self.date = date