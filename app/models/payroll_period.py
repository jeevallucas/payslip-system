from datetime import date

class PayrollPeriodCreate:
    def __init__(self, name: str, start_date: date, end_date: date, created_by: int):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.created_by = created_by