# scripts/seed_employees.py

import psycopg2
import bcrypt
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# DB Connection
conn = psycopg2.connect(
    dbname="db_payslip_system_",
    user="u_jeevallucas",
    password="p_jeevallucas",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def seed_employees(n=100):
    print(f"Seeding {n} employees...")
    for _ in range(n):
        username = fake.user_name()
        full_name = fake.name()
        email = fake.email()
        password = "password123"  # Default password for all
        base_salary = round(random.uniform(30000, 120000), 2)

        hashed_pw = hash_password(password)

        cur.execute("""
            INSERT INTO employees (username, full_name, email, password_hash, base_salary)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, full_name, email, hashed_pw, base_salary))

    conn.commit()
    print("✅ Employees seeded successfully.")

if __name__ == "__main__":
    seed_employees(100)