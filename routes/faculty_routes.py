from datetime import date, datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from auth import faculty_required
from database import db_session
from models import Faculty, Course, Student, Enrollment, Attendance, Assignment, AssignmentSubmission

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

def get_current_faculty():
    """Helper to get current faculty profile."""
    if not current_user.is_authenticated:
        return None
    return db_session.query(Faculty).filter_by(user_id=current_user.id).first()

@faculty_bp.route('/dashboard')
@faculty_required
def dashboard():
    faculty = get_current_faculty()
    if not faculty:
        flash('Faculty profile not found for this account.', 'danger')
        return redirect(url_for('auth.login'))

    courses = db_session.query(Course).filter_by(faculty_id=faculty.id).all()
    course_ids = [c.id for c in courses]

    # Quick metrics
    total_courses = len(courses)
    total_assignments = db_session.query(Assignment).filter_by(faculty_id=faculty.id).count()
    total_attendance_records = db_session.query(Attendance).filter_by(faculty_id=faculty.id).count()

    # Get total enrolled students across all assigned courses
    enrolled_student_ids = set()
    if course_ids:
        enrollments = db_session.query(Enrollment).filter(Enrollment.course_id.in_(course_ids)).all()
        enrolled_student_ids = {e.student_id for e in enrollments}

    # Recent assignments
    recent_assignments = db_session.query(Assignment).filter_by(faculty_id=faculty.id)\
        .order_by(Assignment.created_at.desc()).limit(5).all()

    return render_template(
        'faculty/dashboard.html',
        faculty=faculty,
        courses=courses,
        total_courses=total_courses,
        total_students=len(enrolled_student_ids),
        total_assignments=total_assignments,
        total_attendance_records=total_attendance_records,
        recent_assignments=recent_assignments
    )

# --- ATTENDANCE MANAGEMENT ---

@faculty_bp.route('/attendance', methods=['GET', 'POST'])
@faculty_required
def attendance():
    faculty = get_current_faculty()
    courses = db_session.query(Course).filter_by(faculty_id=faculty.id).all()

    selected_course_id = request.args.get('course_id', type=int)
    selected_date_str = request.args.get('date', date.today().isoformat())

    # Fallback to first assigned course if not selected
    if not selected_course_id and courses:
        selected_course_id = courses[0].id

    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        selected_date = date.today()
        selected_date_str = selected_date.isoformat()

    selected_course = None
    students_with_status = []

    if selected_course_id:
        selected_course = db_session.get(Course, selected_course_id)
        # Ensure faculty is authorized for this course
        if selected_course and selected_course.faculty_id == faculty.id:
            # Enrolled students
            enrollments = db_session.query(Enrollment).filter_by(course_id=selected_course_id).all()
            
            # Existing attendance on selected date
            existing_attendances = db_session.query(Attendance).filter_by(
                course_id=selected_course_id,
                date=selected_date
            ).all()
            att_map = {a.student_id: a for a in existing_attendances}

            for e in enrollments:
                student = e.student
                att_record = att_map.get(student.id)
                status = att_record.status if att_record else 'Present'
                remarks = att_record.remarks if att_record else ''
                students_with_status.append({
                    'student': student,
                    'status': status,
                    'remarks': remarks
                })

    if request.method == 'POST':
        # Batch save/update attendance
        post_course_id = int(request.form.get('course_id'))
        post_date_str = request.form.get('date')
        post_date = datetime.strptime(post_date_str, '%Y-%m-%d').date()

        # Security check: course belongs to faculty
        course_check = db_session.get(Course, post_course_id)
        if not course_check or course_check.faculty_id != faculty.id:
            flash('Unauthorized: You are not assigned to this course.', 'danger')
            return redirect(url_for('faculty.attendance'))

        enrollments = db_session.query(Enrollment).filter_by(course_id=post_course_id).all()

        for e in enrollments:
            s_id = e.student_id
            status_val = request.form.get(f'status_{s_id}', 'Present')
            remarks_val = request.form.get(f'remarks_{s_id}', '').strip()

            record = db_session.query(Attendance).filter_by(
                student_id=s_id,
                course_id=post_course_id,
                date=post_date
            ).first()

            if record:
                record.status = status_val
                record.remarks = remarks_val
                record.faculty_id = faculty.id
            else:
                record = Attendance(
                    student_id=s_id,
                    course_id=post_course_id,
                    faculty_id=faculty.id,
                    date=post_date,
                    status=status_val,
                    remarks=remarks_val
                )
                db_session.add(record)

        db_session.commit()
        flash(f'Attendance successfully recorded for {course_check.course_code} on {post_date_str}.', 'success')
        return redirect(url_for('faculty.attendance', course_id=post_course_id, date=post_date_str))

    return render_template(
        'faculty/attendance.html',
        courses=courses,
        selected_course=selected_course,
        selected_course_id=selected_course_id,
        selected_date_str=selected_date_str,
        students_with_status=students_with_status
    )

# --- ASSIGNMENT MANAGEMENT & GRADING ---

@faculty_bp.route('/assignments', methods=['GET', 'POST'])
@faculty_required
def assignments():
    faculty = get_current_faculty()
    courses = db_session.query(Course).filter_by(faculty_id=faculty.id).all()

    if request.method == 'POST':
        course_id = int(request.form.get('course_id'))
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        max_marks = float(request.form.get('max_marks', 100))
        due_date_str = request.form.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None

        # Verify course belongs to faculty
        course_check = db_session.get(Course, course_id)
        if not course_check or course_check.faculty_id != faculty.id:
            flash('Unauthorized: You can only create assignments for your assigned courses.', 'danger')
            return redirect(url_for('faculty.assignments'))

        new_assignment = Assignment(
            course_id=course_id,
            faculty_id=faculty.id,
            title=title,
            description=description,
            max_marks=max_marks,
            due_date=due_date
        )
        db_session.add(new_assignment)
        db_session.commit()
        flash(f'Assignment "{title}" created successfully.', 'success')
        return redirect(url_for('faculty.assignments'))

    faculty_assignments = db_session.query(Assignment).filter_by(faculty_id=faculty.id)\
        .order_by(Assignment.created_at.desc()).all()

    return render_template(
        'faculty/assignments.html',
        courses=courses,
        assignments=faculty_assignments
    )

@faculty_bp.route('/assignments/<int:assignment_id>/grade', methods=['GET', 'POST'])
@faculty_required
def grade_assignment(assignment_id):
    faculty = get_current_faculty()
    assignment = db_session.get(Assignment, assignment_id)

    if not assignment or assignment.faculty_id != faculty.id:
        flash('Assignment not found or access unauthorized.', 'danger')
        return redirect(url_for('faculty.assignments'))

    enrollments = db_session.query(Enrollment).filter_by(course_id=assignment.course_id).all()
    submissions = db_session.query(AssignmentSubmission).filter_by(assignment_id=assignment.id).all()
    sub_map = {s.student_id: s for s in submissions}

    if request.method == 'POST':
        for e in enrollments:
            s_id = e.student_id
            marks_raw = request.form.get(f'marks_{s_id}')
            remarks = request.form.get(f'remarks_{s_id}', '').strip()

            if marks_raw is not None and marks_raw != '':
                try:
                    marks = float(marks_raw)
                    sub = sub_map.get(s_id)
                    if sub:
                        sub.marks_obtained = marks
                        sub.remarks = remarks
                        sub.submission_status = 'Graded'
                        sub.graded_at = datetime.now(timezone.utc)
                    else:
                        sub = AssignmentSubmission(
                            assignment_id=assignment.id,
                            student_id=s_id,
                            marks_obtained=marks,
                            submission_status='Graded',
                            remarks=remarks
                        )
                        db_session.add(sub)
                except ValueError:
                    pass

        db_session.commit()
        flash('Assignment marks and remarks updated successfully.', 'success')
        return redirect(url_for('faculty.grade_assignment', assignment_id=assignment.id))

    students_grading = []
    for e in enrollments:
        student = e.student
        sub = sub_map.get(student.id)
        students_grading.append({
            'student': student,
            'marks': sub.marks_obtained if sub and sub.marks_obtained is not None else '',
            'remarks': sub.remarks if sub and sub.remarks else '',
            'status': sub.submission_status if sub else 'Pending'
        })

    return render_template(
        'faculty/grade_assignment.html',
        assignment=assignment,
        students_grading=students_grading
    )
