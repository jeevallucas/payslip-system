from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from decimal import Decimal
import psycopg2

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
class ReimbursementCreate(BaseModel):
    amount: float
    description: str = ""

@router.post("/reimbursements", status_code=status.HTTP_201_CREATED)
def submit_reimbursement(
    payload: ReimbursementCreate,
    current_employee: dict = Depends(get_current_employee)
):
    emp_id = current_employee["id"]
    amount = round(payload.amount, 2)

    # Validate positive amount
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reimbursement amount must be greater than zero."
        )

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO reimbursements (employee_id, amount, description, created_by)
            VALUES (%s, %s, %s, %s)
            RETURNING id, created_at
        """, (emp_id, amount, payload.description, emp_id))

        result = cur.fetchone()
        reimb_id, created_at = result
        conn.commit()

        return {
            "id": reimb_id,
            "message": "Reimbursement request successfully recorded.",
            "amount": amount,
            "description": payload.description or "",
            "created_at": created_at
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()