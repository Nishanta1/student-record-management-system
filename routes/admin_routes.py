from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy import inspect, text
from auth import admin_required
from config import Config
from database import db_session, engine
from models import User, Faculty, Student, Course, Enrollment, Attendance, Assignment

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_students = db_session.query(Student).count()
    total_faculty = db_session.query(Faculty).count()
    total_courses = db_session.query(Course).count()
    total_attendance = db_session.query(Attendance).count()
    total_assignments = db_session.query(Assignment).count()

    recent_faculty = db_session.query(Faculty).join(User).order_by(User.created_at.desc()).limit(5).all()
    recent_students = db_session.query(Student).order_by(Student.created_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_faculty=total_faculty,
        total_courses=total_courses,
        total_attendance=total_attendance,
        total_assignments=total_assignments,
        recent_faculty=recent_faculty,
        recent_students=recent_students
    )

# --- FACULTY MANAGEMENT ---

@admin_bp.route('/faculty', methods=['GET', 'POST'])
@admin_required
def faculty_list():
    if request.method == 'POST':
        # Add new faculty member
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        employee_id = request.form.get('employee_id', '').strip()
        department = request.form.get('department', '').strip()
        designation = request.form.get('designation', 'Assistant Professor').strip()
        phone = request.form.get('phone', '').strip()

        # Validation
        if not all([username, password, full_name, email, employee_id, department]):
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('admin.faculty_list'))

        # Check existing username or email
        existing_user = db_session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash('A user with this username or email already exists.', 'danger')
            return redirect(url_for('admin.faculty_list'))

        # Check existing employee id
        existing_emp = db_session.query(Faculty).filter_by(employee_id=employee_id).first()
        if existing_emp:
            flash('A faculty member with this Employee ID already exists.', 'danger')
            return redirect(url_for('admin.faculty_list'))

        # Create user & faculty profile
        new_user = User(
            username=username,
            full_name=full_name,
            email=email,
            role='faculty',
            is_active=True
        )
        new_user.set_password(password)
        db_session.add(new_user)
        db_session.flush()

        new_faculty = Faculty(
            user_id=new_user.id,
            employee_id=employee_id,
            department=department,
            designation=designation,
            phone=phone
        )
        db_session.add(new_faculty)
        db_session.commit()

        flash(f'Faculty member "{full_name}" (Login: {username}) added successfully!', 'success')
        return redirect(url_for('admin.faculty_list'))

    faculties = db_session.query(Faculty).join(User).all()
    return render_template('admin/faculty_list.html', faculties=faculties)

@admin_bp.route('/faculty/toggle/<int:user_id>', methods=['POST'])
@admin_required
def toggle_faculty_status(user_id):
    user = db_session.get(User, user_id)
    if user and user.role == 'faculty':
        user.is_active = not user.is_active
        db_session.commit()
        status_text = 'activated' if user.is_active else 'deactivated'
        flash(f'Faculty account "{user.username}" {status_text}.', 'info')
    return redirect(url_for('admin.faculty_list'))

# --- STUDENT MANAGEMENT ---

@admin_bp.route('/students', methods=['GET', 'POST'])
@admin_required
def student_list():
    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip().upper()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        department = request.form.get('department', '').strip()
        semester = int(request.form.get('semester', 1))
        phone = request.form.get('phone', '').strip()

        if not all([roll_number, name, email, department]):
            flash('Please fill in all required student details.', 'danger')
            return redirect(url_for('admin.student_list'))

        existing_stu = db_session.query(Student).filter(
            (Student.roll_number == roll_number) | (Student.email == email)
        ).first()
        if existing_stu:
            flash('A student with this Roll Number or Email already exists.', 'danger')
            return redirect(url_for('admin.student_list'))

        new_student = Student(
            roll_number=roll_number,
            name=name,
            email=email,
            department=department,
            semester=semester,
            phone=phone
        )
        db_session.add(new_student)
        db_session.commit()
        flash(f'Student "{name}" ({roll_number}) added successfully!', 'success')
        return redirect(url_for('admin.student_list'))

    students = db_session.query(Student).order_by(Student.roll_number).all()
    courses = db_session.query(Course).all()
    return render_template('admin/student_list.html', students=students, courses=courses)

@admin_bp.route('/students/delete/<int:student_id>', methods=['POST'])
@admin_required
def delete_student(student_id):
    student = db_session.get(Student, student_id)
    if student:
        db_session.delete(student)
        db_session.commit()
        flash(f'Student record for "{student.name}" deleted successfully.', 'info')
    return redirect(url_for('admin.student_list'))

# --- COURSE & ALLOCATION MANAGEMENT ---

@admin_bp.route('/courses', methods=['GET', 'POST'])
@admin_required
def course_list():
    if request.method == 'POST':
        course_code = request.form.get('course_code', '').strip().upper()
        course_name = request.form.get('course_name', '').strip()
        department = request.form.get('department', '').strip()
        semester = int(request.form.get('semester', 1))
        faculty_id = request.form.get('faculty_id')
        faculty_id = int(faculty_id) if faculty_id else None

        if not all([course_code, course_name, department]):
            flash('Course Code, Name, and Department are required.', 'danger')
            return redirect(url_for('admin.course_list'))

        existing_course = db_session.query(Course).filter_by(course_code=course_code).first()
        if existing_course:
            flash(f'Course with code {course_code} already exists.', 'danger')
            return redirect(url_for('admin.course_list'))

        new_course = Course(
            course_code=course_code,
            course_name=course_name,
            department=department,
            semester=semester,
            faculty_id=faculty_id
        )
        db_session.add(new_course)
        db_session.commit()
        flash(f'Course "{course_code}: {course_name}" created successfully.', 'success')
        return redirect(url_for('admin.course_list'))

    courses = db_session.query(Course).all()
    faculties = db_session.query(Faculty).join(User).filter(User.is_active == True).all()
    return render_template('admin/course_list.html', courses=courses, faculties=faculties)

@admin_bp.route('/courses/assign', methods=['POST'])
@admin_required
def assign_faculty():
    course_id = int(request.form.get('course_id'))
    faculty_id = request.form.get('faculty_id')
    course = db_session.get(Course, course_id)
    if course:
        course.faculty_id = int(faculty_id) if faculty_id else None
        db_session.commit()
        flash(f'Faculty assignment updated for course {course.course_code}.', 'success')
    return redirect(url_for('admin.course_list'))

@admin_bp.route('/courses/enroll', methods=['POST'])
@admin_required
def enroll_student():
    student_id = int(request.form.get('student_id'))
    course_id = int(request.form.get('course_id'))

    existing = db_session.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()
    if existing:
        flash('Student is already enrolled in this course.', 'warning')
    else:
        enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db_session.add(enrollment)
        db_session.commit()
        flash('Student successfully enrolled in course.', 'success')
    return redirect(url_for('admin.student_list'))

# --- DATABASE INSPECTOR & VIEWER ---

@admin_bp.route('/database', methods=['GET', 'POST'])
@admin_required
def database_viewer():
    inspector = inspect(engine)
    all_tables = sorted(inspector.get_table_names())

    # Get stats for each table
    table_stats = []
    total_records = 0
    with engine.connect() as conn:
        for t in all_tables:
            try:
                cnt = conn.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
            except Exception:
                cnt = 0
            table_stats.append({'name': t, 'count': cnt})
            total_records += cnt

    selected_table = request.args.get('table')
    if not selected_table or selected_table not in all_tables:
        selected_table = all_tables[0] if all_tables else None

    columns_info = []
    foreign_keys = []
    rows = []
    column_names = []
    sql_error = None
    custom_query_results = None
    custom_query_cols = None
    custom_sql = ""

    if selected_table:
        raw_cols = inspector.get_columns(selected_table)
        foreign_keys = inspector.get_foreign_keys(selected_table)
        fk_map = {
            col: f"{fk['referred_table']}.{fk['referred_columns'][0]}"
            for fk in foreign_keys
            for col in fk['constrained_columns']
        }

        for col in raw_cols:
            columns_info.append({
                'name': col['name'],
                'type': str(col['type']),
                'nullable': col.get('nullable', True),
                'primary_key': bool(col.get('primary_key', False)),
                'foreign_key': fk_map.get(col['name'])
            })
            column_names.append(col['name'])

        # Fetch records for selected table (max 100 for safety)
        with engine.connect() as conn:
            try:
                result = conn.execute(text(f"SELECT * FROM {selected_table} LIMIT 100"))
                rows = [dict(row._mapping) for row in result]
            except Exception as e:
                rows = []

    # Handle custom query execution
    if request.method == 'POST':
        custom_sql = request.form.get('sql_query', '').strip()
        if custom_sql:
            first_word = custom_sql.split()[0].upper() if custom_sql.split() else ""
            # Restrict to read-only queries for security
            if first_word not in ['SELECT', 'PRAGMA', 'EXPLAIN', 'SHOW', 'DESCRIBE']:
                sql_error = "For security reasons, only read-only queries (SELECT, PRAGMA, EXPLAIN, SHOW) can be executed here."
            else:
                with engine.connect() as conn:
                    try:
                        res = conn.execute(text(custom_sql))
                        custom_query_cols = list(res.keys())
                        custom_query_results = [dict(row._mapping) for row in res.fetchall()]
                    except Exception as ex:
                        sql_error = str(ex)

    # Sanitize database URI for safe display (mask password if remote)
    db_uri_display = Config.SQLALCHEMY_DATABASE_URI
    if '@' in db_uri_display:
        try:
            prefix, rest = db_uri_display.split('@', 1)
            proto_user = prefix.split(':', 2)
            if len(proto_user) == 3:
                db_uri_display = f"{proto_user[0]}:{proto_user[1]}:******@{rest}"
        except Exception:
            pass

    return render_template(
        'admin/database_viewer.html',
        tables=table_stats,
        selected_table=selected_table,
        columns=columns_info,
        column_names=column_names,
        rows=rows,
        total_records=total_records,
        db_uri=db_uri_display,
        custom_sql=custom_sql,
        custom_query_cols=custom_query_cols,
        custom_query_results=custom_query_results,
        sql_error=sql_error
    )

