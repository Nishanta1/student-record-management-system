from datetime import datetime, timezone, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Text, Float, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def get_utc_now():
    return datetime.now(timezone.utc)

class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    full_name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    role = Column(String(20), nullable=False, default='faculty')  # 'admin' or 'faculty'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=get_utc_now)

    # Relationships
    faculty_profile = relationship('Faculty', back_populates='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_faculty(self):
        return self.role == 'faculty'

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"



class Faculty(Base):
    __tablename__ = 'faculty'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    employee_id = Column(String(32), unique=True, nullable=False)
    department = Column(String(64), nullable=False)
    designation = Column(String(64), default='Assistant Professor')
    phone = Column(String(20), nullable=True)

    # Relationships
    user = relationship('User', back_populates='faculty_profile')
    courses = relationship('Course', back_populates='faculty')
    attendances_marked = relationship('Attendance', back_populates='faculty')
    assignments_created = relationship('Assignment', back_populates='faculty')

    def __repr__(self):
        return f"<Faculty {self.employee_id} - {self.department}>"


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    roll_number = Column(String(32), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    department = Column(String(64), nullable=False)
    semester = Column(Integer, nullable=False, default=1)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    # Relationships
    enrollments = relationship('Enrollment', back_populates='student', cascade='all, delete-orphan')
    attendances = relationship('Attendance', back_populates='student', cascade='all, delete-orphan')
    assignment_submissions = relationship('AssignmentSubmission', back_populates='student', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Student {self.roll_number} - {self.name}>"


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    course_code = Column(String(32), unique=True, nullable=False)
    course_name = Column(String(128), nullable=False)
    department = Column(String(64), nullable=False)
    semester = Column(Integer, nullable=False, default=1)
    faculty_id = Column(Integer, ForeignKey('faculty.id'), nullable=True)

    # Relationships
    faculty = relationship('Faculty', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course', cascade='all, delete-orphan')
    attendances = relationship('Attendance', back_populates='course', cascade='all, delete-orphan')
    assignments = relationship('Assignment', back_populates='course', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Course {self.course_code}: {self.course_name}>"


class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    enrolled_on = Column(Date, default=date.today)

    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')

    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='uq_student_course'),
    )


class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculty.id'), nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    status = Column(String(16), nullable=False, default='Present')  # 'Present', 'Absent', 'Late'
    remarks = Column(String(256), nullable=True)

    student = relationship('Student', back_populates='attendances')
    course = relationship('Course', back_populates='attendances')
    faculty = relationship('Faculty', back_populates='attendances_marked')

    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', 'date', name='uq_attendance_student_course_date'),
    )

    def __repr__(self):
        return f"<Attendance {self.student_id} {self.course_id} {self.date}: {self.status}>"


class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculty.id'), nullable=False)
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    max_marks = Column(Float, nullable=False, default=100.0)
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    course = relationship('Course', back_populates='assignments')
    faculty = relationship('Faculty', back_populates='assignments_created')
    submissions = relationship('AssignmentSubmission', back_populates='assignment', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Assignment {self.title} for {self.course_id}>"


class AssignmentSubmission(Base):
    __tablename__ = 'assignment_submissions'

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    marks_obtained = Column(Float, nullable=True)
    submission_status = Column(String(32), default='Submitted')  # 'Submitted', 'Pending', 'Graded'
    remarks = Column(String(256), nullable=True)
    graded_at = Column(DateTime, default=get_utc_now)

    assignment = relationship('Assignment', back_populates='submissions')
    student = relationship('Student', back_populates='assignment_submissions')

    __table_args__ = (
        UniqueConstraint('assignment_id', 'student_id', name='uq_assignment_student'),
    )

    def __repr__(self):
        return f"<Submission {self.assignment_id} - Student {self.student_id}>"
