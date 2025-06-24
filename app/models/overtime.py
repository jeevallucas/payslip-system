from datetime import date

class OvertimeCreate:
    def __init__(self, employee_id: int, date: date, hours: float):
        self.employee_id = employee_id
        self.date = date
        self.hours = hours