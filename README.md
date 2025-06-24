# Payslip System

A scalable payslip generation system that supports employee attendance, overtime tracking, reimbursement requests, and payroll processing.

---

## 🧾 Overview

This project provides a complete **payslip generation system** with the following features:

- Employee management
- Attendance logging
- Overtime submission
- Reimbursement requests
- Payroll processing
- Payslip generation (individual & summary)
- Admin controls

All operations are based on **monthly payroll periods**, and salaries are calculated based on attendance, prorated base salary, and overtime hours (paid at double rate).

---

## 📦 Technologies Used

- **Python** (FastAPI backend)
- **PostgreSQL** as the main database
- **Pydantic** for request validation
- **Psycopg2** for PostgreSQL interaction
- **Faker** for test data
- **OpenAPI UI** (Swagger) for API documentation

---

## 📁 Project Structure

```
payslip-system/
├── app/
│   ├── routes/            # FastAPI route handlers
│   ├── models/            # ORM-like data models
│   ├── schemas/           # Pydantic schema definitions
│   ├── main.py            # FastAPI entry point
├── db/
│   └── init_db.sql        # PostgreSQL schema setup
├── scripts/
│   ├── seed_employees.py  # Generate fake employees
│   └── seed_admin.py      # Generate admin user
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up PostgreSQL

Make sure PostgreSQL is running:

```bash
sudo service postgresql start
```

Create the database:

```bash
createdb payslip_db -U your_postgres_user
```

Apply DB schema:

```bash
psql -U your_postgres_user -d payslip_db -f db/init_db.sql
```

### 3. Seed Test Data

Run these scripts to generate initial users:

```bash
python scripts/seed_employees.py
python scripts/seed_admin.py
```

---

## 🚀 Run the Server

```bash
uvicorn app.main:app --reload
```

Access the Swagger UI at:

```
http://localhost:8000/docs
```

---

## 🔐 Authentication (Coming Soon)

Authentication will be implemented using **JWT tokens** for both admin and employee roles. For now, a simple hardcoded token placeholder is used in each endpoint.

---

## 🧪 Unit & Integration Testing

We use `pytest` for testing. You can write tests inside a `tests/` folder like this:

```bash
mkdir tests
touch tests/test_attendance.py tests/test_payslip.py ...
```

Use fixtures to mock database connections and authenticated users.

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `GET /` | GET | Welcome message |
| `POST /admin/payroll-periods` | POST | Admin creates a new payroll period |
| `POST /employee/attendance` | POST | Employee submits daily attendance |
| `POST /employee/overtime` | POST | Employee submits overtime hours |
| `POST /employee/reimbursements` | POST | Employee submits reimbursement request |
| `POST /admin/payroll/run` | POST | Admin runs payroll for current period |
| `GET /employee/payslip` | GET | Employee views their payslip |
| `GET /admin/payslip-summary` | GET | Admin views summary of all payslips |

---

## 🏗️ Software Architecture

```
Client (Browser / App)
    ↓
HTTP Requests (JSON)
    ↓
FastAPI (Python)
    ↓
Database Layer (PostgreSQL)
```

### Layers:
- **Presentation Layer**: FastAPI handles HTTP routing and JSON responses.
- **Business Logic Layer**: In-memory logic calculates prorated salary, overtime, and reimbursements.
- **Data Access Layer**: PostgreSQL stores structured data (employees, payroll periods, attendance, etc.).

### Scalability Considerations:
- All endpoints support concurrent access.
- Database indexing ensures fast queries.
- Future plans include caching and async job queues for large-scale payroll processing.

---

## 📈 Performance Scalability

Each functionality should be benchmarked for performance under load. Tools like `locust`, `wrk`, or `JMeter` can simulate high traffic scenarios.

---

## 📜 Audit Logs (Optional Enhancement)

To implement audit logs:
- Add an `audit_logs` table to track changes.
- Use triggers or application logic to log important actions.
- Include fields like:
  - `user_id`
  - `action_type`
  - `request_ip`
  - `request_id`
  - `timestamp`

---

## 🧑‍💻 Author

Developed by Jeevallucas Gautama
GitHub: [github.com/jeevallucas/payslip-system](https://github.com/jeevallucas/payslip-system)
