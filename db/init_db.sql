-- db/init_db.sql

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    password_hash TEXT NOT NULL,
    base_salary NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by INT DEFAULT NULL,
    updated_by INT DEFAULT NULL
);

-- Admin Table
CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    password_hash TEXT NOT NULL,
    role VARCHAR(50) DEFAULT 'admin',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payroll_periods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by INT REFERENCES admins(id),
    updated_by INT REFERENCES admins(id)
);

CREATE TABLE IF NOT EXISTS attendances (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES employees(id),
    date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by INT REFERENCES employees(id),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    updated_by INT REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS overtimes (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES employees(id),
    date DATE NOT NULL,
    hours NUMERIC(4, 2) NOT NULL CHECK (hours > 0 AND hours <= 3),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by INT REFERENCES employees(id),
    updated_by INT REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS reimbursements (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES employees(id),
    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by INT REFERENCES employees(id),
    updated_by INT REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS payslips (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES employees(id),
    payroll_period_id INT NOT NULL REFERENCES payroll_periods(id),
    base_salary NUMERIC(10, 2) NOT NULL,
    attendance_days INT NOT NULL DEFAULT 0,
    overtime_hours NUMERIC(5, 2) NOT NULL DEFAULT 0,
    overtime_amount NUMERIC(10, 2) NOT NULL DEFAULT 0,
    reimbursement_total NUMERIC(10, 2) NOT NULL DEFAULT 0,
    total NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by INT REFERENCES admins(id)
);

-- Optional indexes
CREATE INDEX idx_username ON employees(username);
CREATE INDEX idx_admin_username ON admins(username);

-- Unique constraint: one attendance per day per employee
CREATE UNIQUE INDEX idx_employee_date ON attendances(employee_id, date);

-- Unique constraint: one overtime per day per employee
CREATE UNIQUE INDEX idx_employee_overtime_date ON overtimes(employee_id, date);

-- Ensure one payslip per employee per payroll period
CREATE UNIQUE INDEX idx_employee_payroll_period ON payslips(employee_id, payroll_period_id);