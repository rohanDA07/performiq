import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "performiq.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


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
        employee_id TEXT NOT NULL,
        predicted_score REAL,
        category TEXT,
        department TEXT,
        predicted_at TEXT DEFAULT CURRENT_TIMESTAMP,
        predicted_by TEXT
    );
    """)

    # Seed departments
    depts = ["IT","Finance","Engineering","HR","Sales","Marketing","Operations","Legal","Customer Support"]
    for d in depts:
        c.execute("INSERT OR IGNORE INTO departments (name) VALUES (?)", (d,))

    # Seed default management user
    c.execute("INSERT OR IGNORE INTO management_users (username, password, name, email) VALUES (?,?,?,?)",
              ("admin", _hash("admin123"), "Admin Manager", "admin@company.com"))

    # Seed demo employees
    demo_emps = [
        ("EMP001","john_doe",_hash("emp123"),"John Doe","john@company.com","9876543210",
         30,"Male","IT","Developer","Bachelor",7000,5,92.5,12,40,8,30,1,3.5,3.8),
        ("EMP002","jane_smith",_hash("emp123"),"Jane Smith","jane@company.com","9876543211",
         28,"Female","HR","Analyst","Master",6500,3,88.0,8,38,4,20,0,4.0,4.1),
        ("EMP003","mike_ross",_hash("emp123"),"Mike Ross","mike@company.com","9876543212",
         35,"Male","Finance","Manager","Master",9000,8,95.0,20,45,12,40,2,4.5,4.3),
        ("EMP004","sara_jones",_hash("emp123"),"Sara Jones","sara@company.com","9876543213",
         25,"Female","Sales","Specialist","Bachelor",5500,2,78.0,5,35,2,10,0,2.8,2.5),
    ]
    for e in demo_emps:
        c.execute("""INSERT OR IGNORE INTO employees
            (employee_id,username,password,full_name,email,contact,age,gender,department,
             designation,education_level,salary,experience,attendance_pct,projects_completed,
             working_hours,overtime_hours,training_hours,promotions,previous_rating,satisfaction_score)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", e)

    conn.commit()
    conn.close()


# ── Auth ──────────────────────────────────────────────────────────────────────

def auth_management(username, password):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM management_users WHERE username=? AND password=?",
        (username, _hash(password))
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def auth_employee(username, password):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM employees WHERE username=? AND password=?",
        (username, _hash(password))
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ── Employee CRUD ─────────────────────────────────────────────────────────────

def register_employee(data: dict):
    conn = get_conn()
    try:
        conn.execute("""INSERT INTO employees
            (employee_id,username,password,full_name,email,contact,age,gender,department,
             designation,education_level,salary,experience,attendance_pct,projects_completed,
             working_hours,overtime_hours,training_hours,promotions,previous_rating,satisfaction_score)
            VALUES (:employee_id,:username,:password,:full_name,:email,:contact,:age,:gender,:department,
             :designation,:education_level,:salary,:experience,:attendance_pct,:projects_completed,
             :working_hours,:overtime_hours,:training_hours,:promotions,:previous_rating,:satisfaction_score)""",
            {**data, "password": _hash(data["password"])})
        conn.commit()
        return True, "Registered successfully."
    except sqlite3.IntegrityError as e:
        return False, f"Username or Employee ID already exists."
    finally:
        conn.close()


def get_employee_by_id(employee_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_employee(employee_id, data: dict):
    data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    data["employee_id"] = employee_id
    conn = get_conn()
    conn.execute("""UPDATE employees SET
        full_name=:full_name, email=:email, contact=:contact, age=:age, gender=:gender,
        department=:department, designation=:designation, education_level=:education_level,
        salary=:salary, experience=:experience, attendance_pct=:attendance_pct,
        projects_completed=:projects_completed, working_hours=:working_hours,
        overtime_hours=:overtime_hours, training_hours=:training_hours,
        promotions=:promotions, previous_rating=:previous_rating,
        satisfaction_score=:satisfaction_score, updated_at=:updated_at
        WHERE employee_id=:employee_id""", data)
    conn.commit()
    conn.close()


def delete_employee(employee_id):
    conn = get_conn()
    conn.execute("DELETE FROM employees WHERE employee_id=?", (employee_id,))
    conn.commit()
    conn.close()


def get_all_employees(department=None, search=None):
    conn = get_conn()
    q = "SELECT * FROM employees WHERE 1=1"
    params = []
    if department and department != "All":
        q += " AND department=?"
        params.append(department)
    if search:
        q += " AND (full_name LIKE ? OR employee_id LIKE ? OR department LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    q += " ORDER BY department, full_name"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_departments():
    conn = get_conn()
    rows = conn.execute("SELECT name FROM departments ORDER BY name").fetchall()
    conn.close()
    return [r["name"] for r in rows]


# ── Performance Records ───────────────────────────────────────────────────────

def save_prediction(employee_id, score, category, department, predicted_by="system"):
    conn = get_conn()
    conn.execute("""INSERT INTO performance_records
        (employee_id, predicted_score, category, department, predicted_by)
        VALUES (?,?,?,?,?)""", (employee_id, score, category, department, predicted_by))
    conn.commit()
    conn.close()


def get_predictions(employee_id=None):
    conn = get_conn()
    if employee_id:
        rows = conn.execute(
            "SELECT * FROM performance_records WHERE employee_id=? ORDER BY predicted_at DESC",
            (employee_id,)).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM performance_records ORDER BY predicted_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_dept_stats():
    conn = get_conn()
    rows = conn.execute("""
        SELECT department,
               COUNT(*) as total,
               AVG(salary) as avg_salary,
               AVG(satisfaction_score) as avg_satisfaction,
               AVG(training_hours) as avg_training,
               AVG(attendance_pct) as avg_attendance
        FROM employees GROUP BY department
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_management_user(username, password, name, email):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO management_users (username,password,name,email) VALUES (?,?,?,?)",
                     (username, _hash(password), name, email))
        conn.commit()
        return True, "Management user created."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()
