from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import date
import psycopg2
from typing import Optional

router = APIRouter()

# Fake auth placeholder — future use
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
class AttendanceCreate(BaseModel):
    date: date

@router.post("/attendance", status_code=status.HTTP_201_CREATED)
def submit_attendance(
    payload: AttendanceCreate,
    current_employee: dict = Depends(get_current_employee)
):
    emp_id = current_employee["id"]
    today = payload.date

    # Check if date is a weekend
    if today.weekday() >= 5:  # Saturday = 5, Sunday = 6
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance cannot be submitted on weekends."
        )

    conn = get_db()
    cur = conn.cursor()

    try:
        # Check if already exists
        cur.execute("""
            SELECT id FROM attendances
            WHERE employee_id = %s AND date = %s
        """, (emp_id, today))
        if cur.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendance already recorded for this day."
            )

        # Insert attendance
        cur.execute("""
            INSERT INTO attendances (employee_id, date, created_by)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (emp_id, today, emp_id))

        att_id = cur.fetchone()[0]
        conn.commit()

        return {
            "id": att_id,
            "message": "Attendance successfully recorded.",
            "date": today
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()