# PerformIQ — Employee Intelligence Platform

## Folder Structure
```
PerformIQ/
├── app.py                        ← Main entry point
├── auth.py                       ← Login / register / data storage
├── requirements.txt
├── setup.bat                     ← One-click Windows setup
├── data/                         ← Auto-created on first run
│   ├── users.json
│   └── employees.json
├── pages_custom/
│   ├── login.py                  ← Sign in / Register page
│   ├── employee_dashboard.py     ← Employee profile update
│   └── hr_dashboard.py           ← HR: view all + predict
└── Model/
    └── employee_model.pkl        ← Copy your trained model here
```

## Setup
1. Double-click `setup.bat`
2. Copy your `employee_model.pkl` into the `Model/` folder
3. Run: `streamlit run app.py`

## Demo Credentials
| Role     | Username   | Password |
|----------|------------|----------|
| HR       | hr_admin   | hr123    |
| Employee | john_doe   | emp123   |
| Employee | jane_smith | emp123   |

## Features
- **Sign In / Register** — role-based access
- **Employee Dashboard** — update personal + work details
- **HR Dashboard** — view all employees, stats, predict performance
