import sqlite3
import hashlib
import os
from datetime import datetime

# ==========================================
# DATABASE PATH
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "performiq.db")


# ==========================================
# PASSWORD HASH
# ==========================================

def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ==========================================
# CONNECTION
# ==========================================

def get_conn():

    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def init_db():

    conn = get_conn()

    c = conn.cursor()

    c.executescript("""

    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    );

    CREATE TABLE IF NOT EXISTS management_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id TEXT UNIQUE NOT NULL,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        full_name TEXT NOT NULL,

        email TEXT,

        contact TEXT,

        age INTEGER,

        gender TEXT,

        department TEXT,

        designation TEXT,

        education_level TEXT,

        salary REAL,

        experience INTEGER,

        attendance_pct REAL,

        projects_completed INTEGER,

        working_hours REAL,

        overtime_hours REAL,

        training_hours REAL,

        promotions INTEGER DEFAULT 0,

        previous_rating REAL,

        satisfaction_score REAL,

        created_at TEXT DEFAULT CURRENT_TIMESTAMP,

        updated_at TEXT
    );

    CREATE TABLE IF NOT EXISTS performance_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id TEXT,

        predicted_score REAL,

        category TEXT,

        department TEXT,

        predicted_by TEXT,

        predicted_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    """)

    # ==========================================
    # SEED DEPARTMENTS
    # ==========================================

    depts = [
        "IT",
        "Finance",
        "Engineering",
        "HR",
        "Sales",
        "Marketing",
        "Operations",
        "Legal",
        "Customer Support"
    ]

    for d in depts:

        c.execute(
            "INSERT OR IGNORE INTO departments (name) VALUES (?)",
            (d,)
        )

    # ==========================================
    # DEFAULT ADMIN
    # ==========================================

    c.execute("""
    INSERT OR IGNORE INTO management_users
    (username, password, name, email)
    VALUES (?, ?, ?, ?)
    """, (
        "admin",
        _hash("admin123"),
        "Admin Manager",
        "admin@company.com"
    ))

    # ==========================================
    # DEMO EMPLOYEES
    # ==========================================

    demo_emps = [

        (
            "EMP001",
            "john_doe",
            _hash("emp123"),
            "John Doe",
            "john@company.com",
            "9876543210",
            30,
            "Male",
            "IT",
            "Developer",
            "Bachelor",
            7000,
            5,
            92.5,
            12,
            40,
            8,
            30,
            1,
            3.5,
            3.8
        ),

        (
            "EMP002",
            "jane_smith",
            _hash("emp123"),
            "Jane Smith",
            "jane@company.com",
            "9876543211",
            28,
            "Female",
            "HR",
            "Analyst",
            "Master",
            6500,
            3,
            88.0,
            8,
            38,
            4,
            20,
            0,
            4.0,
            4.1
        ),
    ]

    for e in demo_emps:

        c.execute("""

        INSERT OR IGNORE INTO employees (

            employee_id,
            username,
            password,
            full_name,
            email,
            contact,
            age,
            gender,
            department,
            designation,
            education_level,
            salary,
            experience,
            attendance_pct,
            projects_completed,
            working_hours,
            overtime_hours,
            training_hours,
            promotions,
            previous_rating,
            satisfaction_score

        )

        VALUES (
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,?
        )

        """, e)

    conn.commit()

    conn.close()


# ==========================================
# AUTH
# ==========================================

def auth_management(username, password):

    conn = get_conn()

    row = conn.execute(
        """
        SELECT * FROM management_users
        WHERE username=? AND password=?
        """,
        (username, _hash(password))
    ).fetchone()

    conn.close()

    return dict(row) if row else None


def auth_employee(username, password):

    conn = get_conn()

    row = conn.execute(
        """
        SELECT * FROM employees
        WHERE username=? AND password=?
        """,
        (username, _hash(password))
    ).fetchone()

    conn.close()

    return dict(row) if row else None


# ==========================================
# EMPLOYEE FUNCTIONS
# ==========================================

def get_employee_by_id(employee_id):

    conn = get_conn()

    row = conn.execute(
        """
        SELECT * FROM employees
        WHERE employee_id=?
        """,
        (employee_id,)
    ).fetchone()

    conn.close()

    return dict(row) if row else None


def get_all_employees():

    conn = get_conn()

    rows = conn.execute(
        """
        SELECT * FROM employees
        ORDER BY full_name
        """
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# ==========================================
# PREDICTIONS
# ==========================================

def save_prediction(
    employee_id,
    score,
    category,
    department,
    predicted_by="system"
):

    conn = get_conn()

    conn.execute("""

    INSERT INTO performance_records (

        employee_id,
        predicted_score,
        category,
        department,
        predicted_by

    )

    VALUES (?, ?, ?, ?, ?)

    """, (
        employee_id,
        score,
        category,
        department,
        predicted_by
    ))

    conn.commit()

    conn.close()


def get_predictions(employee_id=None):

    conn = get_conn()

    if employee_id:

        rows = conn.execute(
            """
            SELECT *
            FROM performance_records
            WHERE employee_id=?
            ORDER BY predicted_at DESC
            """,
            (employee_id,)
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT *
            FROM performance_records
            ORDER BY predicted_at DESC
            """
        ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# ==========================================
# AUTO INIT
# ==========================================

init_db()