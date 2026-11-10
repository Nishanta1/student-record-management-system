# 🎓 Student Record Management System (RMS)

A complete, role-based Student Record Management System built with **Python**, **Flask**, and **SQLAlchemy**. It supports running out-of-the-box on a local database (SQLite) or seamlessly connecting to any **Online Cloud Database** (PostgreSQL on Neon/Supabase/Aiven or Remote MySQL).

---

## 🔑 Login Credentials

The system comes pre-seeded with 1 Master Admin account and 3 distinct Faculty accounts with assigned courses:

### 1. Main Admin (Master Permissions)
> Admin has unrestricted access: register/deactivate faculty, enroll students, allocate courses, and manage all master records.

| Role | Username | Password | Full Name | Access Level |
| :--- | :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `Admin@12345` | Master Administrator | **Full System Access** |

---

### 2. Faculty Logins (Restricted Permissions)
> Faculty accounts have strictly scoped permissions: view assigned courses, record & update attendance (Present/Absent/Late), create assignments, and grade student submissions. They cannot access administrative configurations or alter other faculty data.

| Username | Password | Faculty Name | Department | Assigned Course |
| :--- | :--- | :--- | :--- | :--- |
| `faculty.cs` | `Faculty@123` | Prof. Rajesh Sharma | Computer Science | `CS101`: Data Structures & Algorithms |
| `faculty.math` | `Faculty@123` | Dr. Ananya Gupta | Mathematics | `MA102`: Discrete Mathematics |
| `faculty.ai` | `Faculty@123` | Dr. Vikram Verma | Artificial Intelligence | `AI103`: Intro to Machine Learning |

---

## 🗄️ Database Setup & Credentials

### Current Active Database
- **Type**: SQLite (Zero configuration needed)
- **Database File**: `student_records.db`
- **Status**: Pre-seeded with Admin, 3 Faculty members, 5 Students, 3 Courses, and sample attendance/assignment records.

### Connecting to an Online Cloud Database (PostgreSQL / MySQL)
You can switch to any online cloud database provider (such as Neon, Supabase, Aiven, or FreeDB) in seconds.

1. Open `.env` in the project root.
2. Update the `DATABASE_URL` parameter with your cloud connection string:

#### A. Neon Serverless PostgreSQL (https://neon.tech - Free)
```env
DATABASE_URL=postgresql://alex:YourPassword@ep-cool-sample.us-east-2.aws.neon.tech/neondb?sslmode=require
```

#### B. Supabase PostgreSQL (https://supabase.com - Free)
```env
DATABASE_URL=postgresql://postgres:YourPassword@db.abcdefgh.supabase.co:5432/postgres
```

#### C. Aiven / Render / Railway / AWS RDS PostgreSQL
```env
DATABASE_URL=postgresql://dbuser:dbpass@your-cloud-host.aivencloud.com:15432/defaultdb?sslmode=require
```

#### D. Remote MySQL (FreeDB / Remote MySQL)
```env
DATABASE_URL=mysql+pymysql://myuser:mypass@sql.freedb.tech:3306/freedb_student_records
```

> The application automatically creates all necessary tables and re-seeds default admin and faculty credentials upon the first startup on any new database.

---

## 🛡️ Role-Based Access Control (RBAC) Matrix

| Feature / Action | Admin | Faculty |
| :--- | :---: | :---: |
| Access Admin Dashboard & KPI Metrics | ✅ | ❌ |
| Live Database Inspector & SQL Console | ✅ | ❌ |
| Register New Faculty Members | ✅ | ❌ |
| Activate / Deactivate Faculty Accounts | ✅ | ❌ |
| Add / Delete Student Records | ✅ | ❌ |
| Create Courses & Allocate Faculty | ✅ | ❌ |
| Enroll Students into Courses | ✅ | ❌ |
| Access Faculty Teaching Portal | ✅ | ✅ |
| Take & Update Class Attendance | ❌ (View only) | ✅ (Assigned courses) |
| Bulk Mark Attendance (Present / Absent) | ❌ | ✅ |
| Create Coursework / Assignments | ❌ | ✅ (Assigned courses) |
| Grade Student Submissions & Feedback | ❌ | ✅ |

---

## 🔍 How to View Database Structure & Stored Data

### Method 1: Built-in Live Database Inspector (In Web App)
You can inspect the entire database structure and raw data without installing any external software:
1. Log in to the application as **Admin** (`admin` / `Admin@12345`).
2. Click **`DB Inspector`** in the top navigation bar or go directly to:
   ```
   http://127.0.0.1:5000/admin/database
   ```
3. What you can see:
   * **Table Navigator**: Click any table (`users`, `faculty`, `students`, `courses`, `enrollments`, `attendance`, `assignments`, `assignment_submissions`).
   * **Schema Viewer**: Column names, data types (VARCHAR, INTEGER, BOOLEAN, DATETIME), primary keys (PK), and foreign key references (FK).
   * **Live Data Table**: View all records currently saved in that table.
   * **Interactive SQL Console**: Run custom queries (e.g., `SELECT * FROM students;` or complex multi-table `JOIN` statements) and see live results instantly.

---

### Method 2: External GUI Database Viewers (Desktop / Extensions)

#### For Local SQLite (`student_records.db`):
* **DB Browser for SQLite** (Recommended Free Desktop App):
  * Download: [sqlitebrowser.org](https://sqlitebrowser.org/)
  * Open `D:\Antigravity\Project\Student Record management system\student_records.db` to view, query, and edit tables graphically.
* **VS Code / Cursor Extension**:
  * Install the extension **"SQLite Viewer"** (by Florian Klampfer).
  * Right-click `student_records.db` in your file explorer and click *Open with SQLite Viewer*.

#### For Online Cloud Databases (PostgreSQL / MySQL):
* **Neon**: Access the online SQL Editor & Table View directly on [console.neon.tech](https://console.neon.tech).
* **Supabase**: View and edit tables with the Table Editor on [app.supabase.com](https://app.supabase.com).
* **Universal Tools**: Connect using **DBeaver** or **pgAdmin** with your cloud connection credentials.

---

## 🚀 How to Run the Application

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python app.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Quick Login Testing
On the login screen, click any of the **Quick Test Credentials** pill buttons (`Admin`, `Faculty CS`, `Faculty Math`, `Faculty AI`) to automatically fill credentials and sign in instantly.

### 4. Running Verification Tests
Execute the automated test suite to verify role restrictions, authentication, attendance marking, and grading:
```bash
python test_app.py
```
