from fastapi import APIRouter, Depends, HTTPException
import psycopg2
from app.schemas.payslip_summary import PayslipSummarySchema

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

@router.get("/payslip-summary", response_model=PayslipSummarySchema)
def get_payslip_summary(current_admin: dict = Depends(get_current_admin)):
    conn = get_db()
    cur = conn.cursor()

    try:
        # Get latest payroll period (or filter by date if needed)
        cur.execute("SELECT MAX(id) FROM payroll_periods")
        result = cur.fetchone()
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="No payroll periods found.")
        period_id = result[0]

        # Get all payslips for this period
        cur.execute("""
            SELECT employee_id, total FROM payslips
            WHERE payroll_period_id = %s
        """, (period_id,))
        rows = cur.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="No payslips found for this period.")

        employee_summaries = [
            {"employee_id": row[0], "total_take_home": float(row[1])}
            for row in rows
        ]
        grand_total = sum(float(row[1]) for row in rows)

        return {
            "employee_summaries": employee_summaries,
            "grand_total": grand_total
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()