from fastapi import FastAPI
from app.routes import (
    admin,
    attendance,
    overtime,
    reimbursement,
    payroll,
    payslip,
    payslip_summary
)

app = FastAPI(title="Payslip System")

app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(attendance.router, prefix="/employee", tags=["Employee"])
app.include_router(overtime.router, prefix="/employee", tags=["Employee"])
app.include_router(reimbursement.router, prefix="/employee", tags=["Employee"])
app.include_router(payroll.router, prefix="/admin", tags=["Admin"])
app.include_router(payslip.router, prefix="/employee", tags=["Employee"])
app.include_router(payslip_summary.router, prefix="/admin", tags=["Admin"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Payslip System"}