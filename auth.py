import json
import os
import hashlib
from datetime import datetime

# =========================================================
# FILE PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

USERS_PATH = os.path.join(DATA_DIR, "users.json")

EMPLOYEES_PATH = os.path.join(DATA_DIR, "employees.json")

os.makedirs(DATA_DIR, exist_ok=True)

# =========================================================
# PASSWORD HASH
# =========================================================

def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# =========================================================
# DEFAULT USERS
# =========================================================

DEFAULT_USERS = {
    "hr_admin": {
        "password": _hash("hr123"),
        "role": "HR",
        "name": "HR Admin",
        "employee_id": "HR001"
    },

    "john_doe": {
        "password": _hash("emp123"),
        "role": "Employee",
        "name": "John Doe",
        "employee_id": "EMP001"
    },

    "jane_smith": {
        "password": _hash("emp123"),
        "role": "Employee",
        "name": "Jane Smith",
        "employee_id": "EMP002"
    }
}

# =========================================================
# DEFAULT EMPLOYEE DATA
# =========================================================

DEFAULT_EMPLOYEES = {

    "EMP001": {

        "Employee_ID": "EMP001",
        "Name": "John Doe",
        "Department": "IT",
        "Gender": "Male",
        "Job_Title": "Developer",
        "Education_Level": "Bachelor",

        "Age": 30,
        "Years_At_Company": 5,
        "Monthly_Salary": 7000,

        "Work_Hours_Per_Week": 40,
        "Projects_Handled": 12,
        "Overtime_Hours": 8,

        "Training_Hours": 30,
        "Promotions": 1,

        "Employee_Satisfaction_Score": 3.5,

        "last_updated": ""
    },

    "EMP002": {

        "Employee_ID": "EMP002",
        "Name": "Jane Smith",
        "Department": "HR",
        "Gender": "Female",
        "Job_Title": "HR Analyst",
        "Education_Level": "Master",

        "Age": 28,
        "Years_At_Company": 3,
        "Monthly_Salary": 6500,

        "Work_Hours_Per_Week": 38,
        "Projects_Handled": 8,
        "Overtime_Hours": 4,

        "Training_Hours": 20,
        "Promotions": 0,

        "Employee_Satisfaction_Score": 4.0,

        "last_updated": ""
    }
}

# =========================================================
# LOAD USERS
# =========================================================

def _load_users():

    if not os.path.exists(USERS_PATH):

        with open(USERS_PATH, "w") as f:
            json.dump(DEFAULT_USERS, f, indent=4)

    with open(USERS_PATH, "r") as f:
        return json.load(f)

# =========================================================
# SAVE USERS
# =========================================================

def _save_users(data):

    with open(USERS_PATH, "w") as f:
        json.dump(data, f, indent=4)

# =========================================================
# LOAD EMPLOYEES
# =========================================================

def _load_employees():

    if not os.path.exists(EMPLOYEES_PATH):

        with open(EMPLOYEES_PATH, "w") as f:
            json.dump(DEFAULT_EMPLOYEES, f, indent=4)

    with open(EMPLOYEES_PATH, "r") as f:
        return json.load(f)

# =========================================================
# SAVE EMPLOYEES
# =========================================================

def _save_employees(data):

    with open(EMPLOYEES_PATH, "w") as f:
        json.dump(data, f, indent=4)

# =========================================================
# AUTHENTICATION
# =========================================================

def authenticate(username: str, password: str):

    users = _load_users()

    if username in users:

        user = users[username]

        if user["password"] == _hash(password):

            return (
                user["role"],
                user["name"],
                user["employee_id"]
            )

    return None

# =========================================================
# REGISTER EMPLOYEE
# =========================================================

def register_employee(
    username,
    password,
    name,
    employee_id,
    department="IT"
):

    users = _load_users()

    if username in users:
        return False, "Username already exists"

    # ---------- SAVE USER LOGIN ----------

    users[username] = {

        "password": _hash(password),

        "role": "Employee",

        "name": name,

        "employee_id": employee_id
    }

    _save_users(users)

    # ---------- SAVE EMPLOYEE DATA ----------

    employees = _load_employees()

    employees[employee_id] = {

        "Employee_ID": employee_id,

        "Name": name,

        "Department": department,

        "Gender": "",

        "Job_Title": "",

        "Education_Level": "",

        "Age": 25,

        "Years_At_Company": 0,

        "Monthly_Salary": 5000,

        "Work_Hours_Per_Week": 40,

        "Projects_Handled": 0,

        "Overtime_Hours": 0,

        "Training_Hours": 0,

        "Promotions": 0,

        "Employee_Satisfaction_Score": 3.0,

        "last_updated": ""
    }

    _save_employees(employees)

    return True, "Employee Registered Successfully"

# =========================================================
# GET SINGLE EMPLOYEE
# =========================================================

def get_employee(employee_id: str):

    employees = _load_employees()

    return employees.get(employee_id)

# =========================================================
# UPDATE EMPLOYEE
# =========================================================

def update_employee(employee_id: str, updated_data: dict):

    employees = _load_employees()

    if employee_id not in employees:

        return False

    employees[employee_id].update(updated_data)

    employees[employee_id]["last_updated"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    _save_employees(employees)

    return True

# =========================================================
# GET ALL EMPLOYEES
# =========================================================

def get_all_employees():

    return _load_employees()

# =========================================================
# GET EMPLOYEES BY DEPARTMENT
# =========================================================

def get_employees_by_department(department):

    employees = _load_employees()

    filtered = {}

    for emp_id, emp_data in employees.items():

        if emp_data["Department"] == department:

            filtered[emp_id] = emp_data

    return filtered

# =========================================================
# GET ALL DEPARTMENTS
# =========================================================

def get_departments():

    employees = _load_employees()

    departments = set()

    for emp in employees.values():

        departments.add(emp["Department"])

    return sorted(list(departments))