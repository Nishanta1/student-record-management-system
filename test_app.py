import unittest
from app import create_app
from database import init_db, db_session
from models import User, Faculty, Student, Course, Attendance, Assignment, AssignmentSubmission

class TestStudentRecordSystem(unittest.TestCase):
    def setUp(self):
        init_db()
        # Clean up any leftover test faculty
        test_user = db_session.query(User).filter_by(username='faculty.test').first()
        if test_user:
            db_session.delete(test_user)
            db_session.commit()
        test_asg = db_session.query(Assignment).filter_by(title='Test Python Recursion Lab').first()
        if test_asg:
            db_session.delete(test_asg)
            db_session.commit()

        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    def tearDown(self):
        db_session.remove()

    def test_01_unauthorized_redirect(self):
        """Unauthenticated user should be redirected to login."""
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_02_admin_login_and_add_faculty(self):
        """Admin can log in and register a new faculty member."""
        # 1. Login as Admin
        login_resp = self.client.post('/login', data={
            'username': 'admin',
            'password': 'Admin@12345'
        }, follow_redirects=True)
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn(b'Admin Master Dashboard', login_resp.data)

        # 2. Add new faculty
        new_fac_username = 'faculty.test'
        add_resp = self.client.post('/admin/faculty', data={
            'username': new_fac_username,
            'password': 'TestPass@123',
            'full_name': 'Dr. Test Professor',
            'email': 'testprof@university.edu',
            'employee_id': 'FAC-TEST-999',
            'department': 'Computer Science',
            'designation': 'Assistant Professor',
            'phone': '+1-555-9999'
        }, follow_redirects=True)
        self.assertEqual(add_resp.status_code, 200)
        self.assertIn(b'added successfully', add_resp.data)

        # 3. Verify user in DB
        user = db_session.query(User).filter_by(username=new_fac_username).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('TestPass@123'))
        self.assertEqual(user.role, 'faculty')

    def test_03_faculty_permission_restrictions(self):
        """Faculty cannot access admin endpoints."""
        # Login as faculty.cs
        self.client.post('/login', data={
            'username': 'faculty.cs',
            'password': 'Faculty@123'
        }, follow_redirects=True)

        # Attempt to access /admin/faculty
        admin_page_resp = self.client.get('/admin/faculty', follow_redirects=True)
        self.assertIn(b'Access restricted', admin_page_resp.data)

    def test_04_faculty_attendance_and_assignments(self):
        """Faculty can mark attendance and grade assignments."""
        # Login as faculty.cs
        self.client.post('/login', data={
            'username': 'faculty.cs',
            'password': 'Faculty@123'
        }, follow_redirects=True)

        # Fetch CS101 course
        cs_course = db_session.query(Course).filter_by(course_code='CS101').first()
        self.assertIsNotNone(cs_course)

        # 1. Mark attendance
        att_resp = self.client.post('/faculty/attendance', data={
            'course_id': cs_course.id,
            'date': '2026-10-24',
            'status_1': 'Present',
            'remarks_1': 'Present on time'
        }, follow_redirects=True)
        self.assertEqual(att_resp.status_code, 200)
        self.assertIn(b'Attendance successfully recorded', att_resp.data)

        # 2. Create assignment
        asg_resp = self.client.post('/faculty/assignments', data={
            'course_id': cs_course.id,
            'title': 'Test Python Recursion Lab',
            'description': 'Solve towers of Hanoi',
            'max_marks': 50,
            'due_date': '2026-10-30'
        }, follow_redirects=True)
        self.assertEqual(asg_resp.status_code, 200)
        self.assertIn(b'created successfully', asg_resp.data)

        # Verify assignment in DB
        asg = db_session.query(Assignment).filter_by(title='Test Python Recursion Lab').first()
        self.assertIsNotNone(asg)

        # 3. Grade assignment
        grade_resp = self.client.post(f'/faculty/assignments/{asg.id}/grade', data={
            'marks_1': '48.5',
            'remarks_1': 'Great logic and recursion base condition'
        }, follow_redirects=True)
        self.assertEqual(grade_resp.status_code, 200)
        self.assertIn(b'Assignment marks and remarks updated successfully', grade_resp.data)

    def test_05_database_inspector(self):
        """Admin can inspect database schema and stored records; faculty is blocked."""
        # 1. Faculty attempt -> blocked
        self.client.post('/login', data={'username': 'faculty.cs', 'password': 'Faculty@123'}, follow_redirects=True)
        fac_resp = self.client.get('/admin/database', follow_redirects=True)
        self.assertIn(b'Access restricted', fac_resp.data)

        # 2. Admin attempt -> succeeds
        self.client.get('/logout', follow_redirects=True)
        self.client.post('/login', data={'username': 'admin', 'password': 'Admin@12345'}, follow_redirects=True)
        admin_resp = self.client.get('/admin/database?table=users', follow_redirects=True)
        self.assertEqual(admin_resp.status_code, 200)
        self.assertIn(b'Live Database Inspector', admin_resp.data)
        self.assertIn(b'users', admin_resp.data)
        self.assertIn(b'admin@university.edu', admin_resp.data)

        # 3. Execute custom SQL query
        sql_resp = self.client.post('/admin/database', data={
            'sql_query': 'SELECT username, role FROM users WHERE role = "admin"'
        }, follow_redirects=True)
        self.assertEqual(sql_resp.status_code, 200)
        self.assertIn(b'Query Results', sql_resp.data)

if __name__ == '__main__':
    unittest.main()
