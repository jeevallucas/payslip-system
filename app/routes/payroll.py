from fastapi import APIRouter, Depends, HTTPException, status
import psycopg2
from app.schemas.payroll import ProcessPayrollRequest, PayslipResponse

router = APIRouter()

# Fake auth placeholder — will be replaced later
def get_current_admin():
    return {"id": 1}  # Simulated authenticated admin ID

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

@router.post("/payroll/run", status_code=status.HTTP_201_CREATED)
def run_payroll(
    payload: ProcessPayrollRequest,
    current_admin: dict = Depends(get_current_admin)
):
    period_id = payload.payroll_period_id
    admin_id = current_admin["id"]

    conn = get_db()
    cur = conn.cursor()

    try:
        # Check if this payroll has already been run
        cur.execute("""
            SELECT COUNT(*) FROM payslips WHERE payroll_period_id = %s
        """, (period_id,))
        if cur.fetchone()[0] > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payroll for this period has already been processed."
            )

        # Get payroll period dates
        cur.execute("""
            SELECT start_date, end_date FROM payroll_periods WHERE id = %s
        """, (period_id,))
        period = cur.fetchone()
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payroll period not found."
            )
        start_date, end_date = period

        # Get all employees
        cur.execute("SELECT id, base_salary FROM employees")
        employees = cur.fetchall()

        payslips = []

        for emp_id, base_salary in employees:
            # Count attendance
            cur.execute("""
                SELECT COUNT(*) FROM attendances
                WHERE employee_id = %s AND date BETWEEN %s AND %s
            """, (emp_id, start_date, end_date))
            attendance_days = cur.fetchone()[0]

            # Sum overtime hours
            cur.execute("""
                SELECT COALESCE(SUM(hours), 0) FROM overtimes
                WHERE employee_id = %s AND date BETWEEN %s AND %s
            """, (emp_id, start_date, end_date))
            overtime_hours = float(cur.fetchone()[0])

            # Calculate daily salary and overtime pay
            work_days_in_month = 22  # Approximate working days/month
            daily_salary = base_salary / work_days_in_month
            hourly_rate = daily_salary / 8  # 8-hour workday
            overtime_amount = round(overtime_hours * hourly_rate * 2, 2)

            # Sum reimbursements
            cur.execute("""
                SELECT COALESCE(SUM(amount), 0) FROM reimbursements
                WHERE employee_id = %s AND created_at BETWEEN %s AND %s
            """, (emp_id, start_date, end_date))
            reimbursement_total = float(cur.fetchone()[0])

            # Total
            total = round(
                attendance_days * daily_salary + overtime_amount + reimbursement_total,
                2
            )

            # Insert payslip
            cur.execute("""
                INSERT INTO payslips (
                    employee_id, payroll_period_id, base_salary,
                    attendance_days, overtime_hours, overtime_amount,
                    reimbursement_total, total, created_by
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, created_at
            """, (
                emp_id, period_id, base_salary,
                attendance_days, overtime_hours, overtime_amount,
                reimbursement_total, total, admin_id
            ))
            payslip_id, created_at = cur.fetchone()

            payslips.append({
                "id": payslip_id,
                "employee_id": emp_id,
                "payroll_period_id": period_id,
                "base_salary": base_salary,
                "attendance_days": attendance_days,
                "overtime_hours": overtime_hours,
                "overtime_amount": overtime_amount,
                "reimbursement_total": reimbursement_total,
                "total": total,
                "created_at": created_at
            })

        conn.commit()

        return {
            "message": f"Payroll processed successfully for {len(payslips)} employees.",
            "data": payslips
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()