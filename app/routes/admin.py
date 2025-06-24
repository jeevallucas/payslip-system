from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import date
import psycopg2

router = APIRouter()

# Simple In-Memory Auth for now
AUTHORIZED_ADMIN_ID = 1  # From our seeded admin

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

# Input Schema
class PayrollPeriodCreate(BaseModel):
    name: str
    start_date: date
    end_date: date

# Fake JWT Dependency (for future use)
def get_current_admin():
    return {"id": AUTHORIZED_ADMIN_ID}

@router.post("/payroll-periods", status_code=status.HTTP_201_CREATED)
def create_payroll_period(
    period: PayrollPeriodCreate,
    current_admin: dict = Depends(get_current_admin)
):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO payroll_periods (name, start_date, end_date, created_by)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (period.name, period.start_date, period.end_date, current_admin["id"]))
        period_id = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

    return {
        "id": period_id,
        "message": "Payroll period created successfully",
        "data": period
    }