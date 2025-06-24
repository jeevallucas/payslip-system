# scripts/seed_admin.py

import psycopg2
import bcrypt
from faker import Faker

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

def seed_admin():
    print("Seeding one admin...")
    username = "admin_user"
    full_name = "Admin User"
    email = "admin@example.com"
    password = "admin_pass123"

    hashed_pw = hash_password(password)

    cur.execute("""
        INSERT INTO admins (username, full_name, email, password_hash)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (username) DO NOTHING
    """, (username, full_name, email, hashed_pw))

    conn.commit()
    print("✅ Admin seeded successfully.")

if __name__ == "__main__":
    seed_admin()