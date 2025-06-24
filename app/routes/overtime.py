from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import date
import psycopg2
from typing import Optional

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

# Request schema
class OvertimeCreate(BaseModel):
    date: date
    hours: float

@router.post("/overtime", status_code=status.HTTP_201_CREATED)
def submit_overtime(
    payload: OvertimeCreate,
    current_employee: dict = Depends(get_current_employee)
):
    emp_id = current_employee["id"]
    today = date.today()
    ot_date = payload.date
    ot_hours = round(payload.hours, 2)

    # Rule: Cannot propose overtime for future dates
    if ot_date > today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Overtime cannot be proposed for future dates."
        )

    # Rule: Max 3 hours per day
    if ot_hours > 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Overtime cannot exceed 3 hours per day."
        )

    # Rule: Must be positive
    if ot_hours <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Overtime hours must be greater than zero."
        )

    conn = get_db()
    cur = conn.cursor()

    try:
        # Check if already exists
        cur.execute("""
            SELECT id FROM overtimes
            WHERE employee_id = %s AND date = %s
        """, (emp_id, ot_date))
        if cur.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Overtime already recorded for this day."
            )

        # Insert overtime
        cur.execute("""
            INSERT INTO overtimes (employee_id, date, hours, created_by)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (emp_id, ot_date, ot_hours, emp_id))

        ot_id = cur.fetchone()[0]
        conn.commit()

        return {
            "id": ot_id,
            "message": "Overtime successfully recorded.",
            "date": ot_date,
            "hours": ot_hours
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()