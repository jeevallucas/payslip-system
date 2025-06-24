from fastapi import APIRouter, Depends, HTTPException, status
import psycopg2
from app.schemas.payslip import PayslipDetailSchema

router = APIRouter()

# Fake auth placeholder — will be replaced later
def get_current_employee():
    return {"id": 1}  # Simulated authenticated employee ID

# DB Connection Helper
def get_db():
    conn = psycopg2.connect(
        dbname="db_payslip_system_",
        user="u_jeevallucas",
        password="p_jeevallucas",
        host="localhost",
        port="5432"
    )
    return conn

@router.get("/payslip", response_model=PayslipDetailSchema)
def generate_payslip(current_employee: dict = Depends(get_current_employee)):
    emp_id = current_employee["id"]

    conn = get_db()
    cur = conn.cursor()

    try:
        # Get latest payroll period (or filter by date if needed)
        cur.execute("SELECT MAX(id) FROM payroll_periods")
        result = cur.fetchone()
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="No payroll periods found.")

        period_id = result[0]

        # Get period dates
        cur.execute("SELECT start_date, end_date FROM payroll_periods WHERE id = %s", (period_id,))
        start_date, end_date = cur.fetchone()

        # Base Salary
        cur.execute("SELECT base_salary FROM employees WHERE id = %s", (emp_id,))
        base_salary_row = cur.fetchone()
        if not base_salary_row:
            raise HTTPException(status_code=404, detail="Employee not found.")
        base_salary = base_salary_row[0]

        # Attendance
        cur.execute("""
            SELECT date FROM attendances
            WHERE employee_id = %s AND date BETWEEN %s AND %s
        """, (emp_id, start_date, end_date))
        attendance_details = [{"date": r[0]} for r in cur.fetchall()]
        attendance_days = len(attendance_details)

        # Overtime
        cur.execute("""
            SELECT date, hours FROM overtimes
            WHERE employee_id = %s AND date BETWEEN %s AND %s
        """, (emp_id, start_date, end_date))
        overtime_details = [{"date": r[0], "hours": float(r[1])} for r in cur.fetchall()]
        overtime_hours = sum(float(r["hours"]) for r in overtime_details)

        # Calculate hourly rate and overtime pay
        work_days_in_month = 22
        daily_salary = base_salary / work_days_in_month
        hourly_rate = daily_salary / 8
        overtime_amount = round(overtime_hours * hourly_rate * 2, 2)

        # Reimbursements
        cur.execute("""
            SELECT id, amount, description, created_at FROM reimbursements
            WHERE employee_id = %s AND created_at BETWEEN %s AND %s
        """, (emp_id, start_date, end_date))
        reimbursement_details = [
            {
                "id": r[0],
                "amount": float(r[1]),
                "description": r[2],
                "created_at": str(r[3])
            } for r in cur.fetchall()
        ]
        reimbursement_total = sum(float(r["amount"]) for r in reimbursement_details)

        # Total Pay
        total = round(
            attendance_days * daily_salary + overtime_amount + reimbursement_total,
            2
        )

        return {
            "employee_id": emp_id,
            "base_salary": base_salary,
            "attendance_days": attendance_days,
            "attendance_details": attendance_details,
            "overtime_hours": overtime_hours,
            "overtime_amount": overtime_amount,
            "overtime_details": overtime_details,
            "reimbursements": reimbursement_details,
            "reimbursement_total": reimbursement_total,
            "total": total
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()