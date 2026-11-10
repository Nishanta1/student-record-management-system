from datetime import date, timedelta
from models import User, Faculty, Student, Course, Enrollment, Attendance, Assignment, AssignmentSubmission

def seed_database(session):
    # Check if admin already exists
    admin = session.query(User).filter_by(username='admin').first()
    if admin:
        return  # Database already seeded

    print(">>> Seeding database with initial users, faculty, students, and courses...")

    # 1. Main Admin User
    admin = User(
        username='admin',
        full_name='Master Administrator',
        email='admin@university.edu',
        role='admin',
        is_active=True
    )
    admin.set_password('Admin@12345')
    session.add(admin)

    # 2. Three Faculty Users
    faculty_specs = [
        {
            'username': 'faculty.cs',
            'password': 'Faculty@123',
            'full_name': 'Prof. Rajesh Sharma',
            'email': 'rsharma@university.edu',
            'emp_id': 'FAC-CS-001',
            'department': 'Computer Science',
            'designation': 'Associate Professor',
            'phone': '+1-555-0101'
        },
        {
            'username': 'faculty.math',
            'password': 'Faculty@123',
            'full_name': 'Dr. Ananya Gupta',
            'email': 'agupta@university.edu',
            'emp_id': 'FAC-MA-002',
            'department': 'Mathematics',
            'designation': 'Assistant Professor',
            'phone': '+1-555-0102'
        },
        {
            'username': 'faculty.ai',
            'password': 'Faculty@123',
            'full_name': 'Dr. Vikram Verma',
            'email': 'vverma@university.edu',
            'emp_id': 'FAC-AI-003',
            'department': 'Artificial Intelligence',
            'designation': 'Senior Lecturer',
            'phone': '+1-555-0103'
        }
    ]

    faculty_entities = []
    for spec in faculty_specs:
        user = User(
            username=spec['username'],
            full_name=spec['full_name'],
            email=spec['email'],
            role='faculty',
            is_active=True
        )
        user.set_password(spec['password'])
        session.add(user)
        session.flush()

        faculty = Faculty(
            user_id=user.id,
            employee_id=spec['emp_id'],
            department=spec['department'],
            designation=spec['designation'],
            phone=spec['phone']
        )
        session.add(faculty)
        faculty_entities.append(faculty)

    session.flush()

    # 3. Courses
    courses = [
        Course(
            course_code='CS101',
            course_name='Data Structures & Algorithms',
            department='Computer Science',
            semester=3,
            faculty_id=faculty_entities[0].id
        ),
        Course(
            course_code='MA102',
            course_name='Discrete Mathematics',
            department='Mathematics',
            semester=3,
            faculty_id=faculty_entities[1].id
        ),
        Course(
            course_code='AI103',
            course_name='Intro to Machine Learning',
            department='Artificial Intelligence',
            semester=3,
            faculty_id=faculty_entities[2].id
        )
    ]
    for c in courses:
        session.add(c)
    session.flush()

    # 4. Students
    students_data = [
        ('STU202601', 'Aarav Mehta', 'aarav.mehta@student.edu', 'Computer Science', 3, '+1-555-0201'),
        ('STU202602', 'Diya Patel', 'diya.patel@student.edu', 'Computer Science', 3, '+1-555-0202'),
        ('STU202603', 'Rohan Iyer', 'rohan.iyer@student.edu', 'Artificial Intelligence', 3, '+1-555-0203'),
        ('STU202604', 'Sneha Nair', 'sneha.nair@student.edu', 'Mathematics', 3, '+1-555-0204'),
        ('STU202605', 'Kabir Sen', 'kabir.sen@student.edu', 'Computer Science', 3, '+1-555-0205'),
    ]

    student_entities = []
    for roll, name, email, dept, sem, phone in students_data:
        s = Student(
            roll_number=roll,
            name=name,
            email=email,
            department=dept,
            semester=sem,
            phone=phone
        )
        session.add(s)
        student_entities.append(s)
    session.flush()

    # 5. Enroll Students in Courses
    # CS Students in CS101 and MA102
    # AI Student in CS101, MA102, AI103
    enrollment_mappings = [
        (student_entities[0], courses[0]),
        (student_entities[0], courses[1]),
        (student_entities[1], courses[0]),
        (student_entities[1], courses[1]),
        (student_entities[2], courses[0]),
        (student_entities[2], courses[2]),
        (student_entities[3], courses[1]),
        (student_entities[4], courses[0]),
        (student_entities[4], courses[2]),
    ]
    for stu, crs in enrollment_mappings:
        session.add(Enrollment(student_id=stu.id, course_id=crs.id))
    session.flush()

    # 6. Sample Assignments created by Faculty
    asg1 = Assignment(
        course_id=courses[0].id,
        faculty_id=faculty_entities[0].id,
        title='Lab 1: Binary Search Tree Operations',
        description='Implement insert, search, and AVL balancing in Python.',
        max_marks=100.0,
        due_date=date.today() + timedelta(days=7)
    )
    asg2 = Assignment(
        course_id=courses[1].id,
        faculty_id=faculty_entities[1].id,
        title='Problem Set 1: Graph Theory & Combinatorics',
        description='Solve problems 1 through 10 from Chapter 4 on Graph coloring.',
        max_marks=50.0,
        due_date=date.today() + timedelta(days=5)
    )
    asg3 = Assignment(
        course_id=courses[2].id,
        faculty_id=faculty_entities[2].id,
        title='Mini Project: Linear Regression from Scratch',
        description='Build simple linear regression using NumPy with cost function plot.',
        max_marks=100.0,
        due_date=date.today() + timedelta(days=10)
    )
    session.add_all([asg1, asg2, asg3])
    session.flush()

    # 7. Sample Attendance Records for recent days
    today = date.today()
    yesterday = today - timedelta(days=1)

    # For CS101
    cs_students = [student_entities[0], student_entities[1], student_entities[2], student_entities[4]]
    for idx, stu in enumerate(cs_students):
        status = 'Present' if idx != 1 else 'Absent'
        session.add(Attendance(
            student_id=stu.id,
            course_id=courses[0].id,
            faculty_id=faculty_entities[0].id,
            date=yesterday,
            status=status,
            remarks='On-time' if status == 'Present' else 'Medical leave'
        ))

    # 8. Sample Assignment Submissions
    session.add(AssignmentSubmission(
        assignment_id=asg1.id,
        student_id=student_entities[0].id,
        marks_obtained=95.0,
        submission_status='Graded',
        remarks='Excellent clean code with full tests'
    ))
    session.add(AssignmentSubmission(
        assignment_id=asg1.id,
        student_id=student_entities[1].id,
        marks_obtained=82.0,
        submission_status='Graded',
        remarks='Good implementation, edge cases missed'
    ))

    session.commit()
    print(">>> Seeding completed successfully!")
