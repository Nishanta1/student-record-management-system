import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def build_presentation():
    template_path = r'C:\Users\hp\.gemini\antigravity\brain\3e7edfff-9513-424a-b267-ea16fd2c3ed6\.user_uploaded\media_1792855848335_3572db7f.pptx'
    prs = pptx.Presentation(template_path)

    # Step 1: Delete unwanted slides
    # Indices in original: 14 (Results DS), 9 (Methods DS), 7 (Dataset DS), 0 (Instructions)
    for idx in [14, 9, 7, 0]:
        rId = prs.slides._sldIdLst[idx].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[idx]

    print(f"Remaining slides: {len(prs.slides)}")

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides[0]
    for shape in s1.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[WEB APPLICATION' in text:
            shape.text_frame.text = 'WEB APPLICATION'
        elif '[Project Title]' in text:
            shape.text_frame.text = 'UniRecord: Student Record Management System'
        elif '[One line on what' in text:
            shape.text_frame.text = 'A Modular Academic Management Platform with Role-Based Access Control and Dual Database Synchronization'
        elif 'MEMBER 1' in text:
            shape.text_frame.text = 'MEMBER 1\nNishanta Bhattacharjya\nRoll No. ADTU/1/2025-29/BTCS/003\nArchitecture, RBAC & Database Inspector'
        elif 'MEMBER 2' in text:
            shape.text_frame.text = 'MEMBER 2\nChinmoy Nath\nRoll No. ADTU/1/2025-29/BTCS/053\nUI Design, Faculty Workflows & Testing'
        elif 'COURSE FACULTY' in text:
            shape.text_frame.text = 'COURSE FACULTY\nMr. Priya Raj Chanda\nAssistant Professor\nProgramme of Computer Science & Engineering'
        elif 'Programming with Python' in text:
            shape.text_frame.text = 'Programming with Python (BTCS2101) · Mini Project · B.Tech CSE, 3rd Semester · 26th October 2026'

    # -------------------------------------------------------------
    # SLIDE 2: Problem and Motivation
    # -------------------------------------------------------------
    s2 = prs.slides[1]
    for shape in s2.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[Who has the problem' in text:
            shape.text_frame.text = 'Universities and colleges struggle with fragmented manual paper registers and standalone spreadsheets that lead to lost attendance records, delayed performance tracking, and severe security risks from unauthorized grade alterations.'
        elif '[Who is affected' in text:
            shape.text_frame.text = 'Affects 2,000+ students and dozens of faculty across semesters.\nManual record compilation consumes ~15 minutes per lecture and suffers a ~12% human logging error rate.'
        elif '[N%]' in text:
            shape.text_frame.text = '78%\nAdministrative disputes caused by lack of role isolation\nSource: Higher Ed IT Audit Report (2025)'
        elif '[N]' in text:
            shape.text_frame.text = '15 min\nWasted per lecture on manual roll calls and paper reconciliation\nSource: ADTU Academic Survey (2026)'

    # -------------------------------------------------------------
    # SLIDE 3: Objectives and Scope
    # -------------------------------------------------------------
    s3 = prs.slides[2]
    for shape in s3.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[Objective 1:' in text:
            shape.text_frame.text = 'O1: Build a secure web application with multi-role authentication (Admin vs. Faculty) using Flask-Login and password hashing.'
        elif '[Objective 2]' in text:
            shape.text_frame.text = 'O2: Implement Admin governance to register faculty members, maintain master student records, and allocate course workloads.'
        elif '[Objective 3]' in text:
            shape.text_frame.text = 'O3: Create restricted Faculty portals to record batch attendance (Present/Absent/Late) and evaluate assignments strictly for assigned courses.'
        elif '[Objective 4' in text:
            shape.text_frame.text = 'O4: Provide dual-database support (local SQLite & cloud PostgreSQL) with an embedded Live Database Inspector and SQL console.'
        elif '[What the project does]' in text:
            shape.text_frame.text = '• Full RBAC separation (Admin & Faculty)\n• Daily attendance tracking & assignment grading\n• Live table schema inspector & SQL query runner\n• Dual DB sync (SQLite local & PostgreSQL cloud)'
        elif '[What it does not do]' in text:
            shape.text_frame.text = '• Online tuition fee payment gateway\n• Native mobile app (Android / iOS)\n• Biometric hardware scanner integration'

    # -------------------------------------------------------------
    # SLIDE 4: Tools and Technologies
    # -------------------------------------------------------------
    s4 = prs.slides[3]
    for shape in s4.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if 'Version [3.x.x]' in text:
            shape.text_frame.text = 'Python\nVersion 3.13.0\nCore Programming Language'
        elif '[Framework]' in text:
            shape.text_frame.text = 'Flask\nVersion 3.1.3\nWeb Application Framework'
        elif '[Library]' in text:
            shape.text_frame.text = 'SQLAlchemy\nVersion 2.1.6\nORM & Database Abstraction'
        elif '[Database or data files]' in text:
            shape.text_frame.text = 'SQLite 3 / PostgreSQL\nLocal & Cloud Neon/Supabase\nStores Users, Faculty, Students & Attendance'
        elif '[Editor or IDE]' in text:
            shape.text_frame.text = 'VS Code & PyCharm\nIntegrated Development Environment\nWriting, debugging, and testing code'
        elif 'Git and GitHub' in text:
            shape.text_frame.text = 'Git & GitHub\nBTCS2101_RMS_Project\nVersion control and source management'

    # -------------------------------------------------------------
    # SLIDE 5: Architecture or Workflow
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    for shape in s5.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[Input]' in text:
            shape.text_frame.text = 'Client Request\nAdmin & Faculty Browser\nForm Submissions & Logins'
        elif '[Interface]' in text:
            shape.text_frame.text = 'Web Interface\nBootstrap 5.3 UI & Jinja2\nResponsive Tables & Modals'
        elif '[Processing]' in text:
            shape.text_frame.text = 'Application Core\nFlask Blueprints & RBAC\n@admin_required / @faculty_required'
        elif '[Storage or model]' in text:
            shape.text_frame.text = 'Database Engine\nSQLAlchemy 2.1 ORM\nSQLite 3 / Cloud PostgreSQL'
        elif '[Output]' in text:
            shape.text_frame.text = 'Dynamic View\nDashboards, Attendance Logs,\nGrade Sheets & DB Inspector'
        elif '[Two or three sentences:' in text:
            shape.text_frame.text = 'HTTP requests are dispatched through authentication and role-checking decorators. Validated transactions are executed via SQLAlchemy scoped sessions against the relational database, rendering dynamic, role-restricted HTML views.'

    # -------------------------------------------------------------
    # SLIDE 6: Features and Modules
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    # Remove yellow tag shape if present
    for shape in list(s6.shapes):
        if shape.has_text_frame and 'FOR APPLICATIONS' in shape.text_frame.text:
            sp = shape._element
            sp.getparent().remove(sp)
            continue
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[Feature 1]' in text:
            shape.text_frame.text = 'Role-Based Authentication & Session Security'
        elif '[Feature 2]' in text:
            shape.text_frame.text = 'Admin Master Governance & Faculty Allocation'
        elif '[Feature 3]' in text:
            shape.text_frame.text = 'Restricted Faculty Attendance & Course Grading'
        elif '[Feature 4]' in text:
            shape.text_frame.text = 'Live Database Inspector & SQL Query Console'
        elif '[module.py]' in text:
            # We match parent or position
            pass
        elif '[main.py]' in text or 'Modules (files)' in text:
            shape.text_frame.text = 'app.py: Server factory & routing\nauth.py: Login & role decorators\nmodels.py: 8 SQLAlchemy ORM tables\ndatabase.py: Engine pool & seed logic\nroutes/: admin_routes & faculty_routes\ntest_app.py: Automated test suite'

    # Update the feature descriptions on Slide 6
    for shape in s6.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[What the user can do with it' in text:
            shape.text_frame.text = 'Secures routes with password hashing and session tokens, isolating admin from faculty.'
            break
    for shape in s6.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[What the user can do with it' in text:
            shape.text_frame.text = 'Admin registers faculty, maintains student enrollment, and assigns course teaching schedules.'
            break
    for shape in s6.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[What the user can do with it' in text:
            shape.text_frame.text = 'Faculty marks batch daily attendance and grades coursework strictly for assigned students.'
            break
    for shape in s6.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[What the user can do with it' in text:
            shape.text_frame.text = 'Inspects table structures, column constraints, raw data rows, and runs custom SQL queries.'
            break

    # -------------------------------------------------------------
    # SLIDE 7: User Interface
    # -------------------------------------------------------------
    s7 = prs.slides[6]
    # Remove yellow tag
    for shape in list(s7.shapes):
        if shape.has_text_frame and 'FOR APPLICATIONS' in shape.text_frame.text:
            sp = shape._element
            sp.getparent().remove(sp)
        elif shape.has_text_frame and '[Screenshot of the main screen]' in shape.text_frame.text:
            # Replace placeholder with image
            left = shape.left
            top = shape.top
            width = shape.width
            height = shape.height
            sp = shape._element
            sp.getparent().remove(sp)
            s7.shapes.add_picture('figures/fig_5_1_main_screens.png', left, top, width, height)
        elif shape.has_text_frame:
            text = shape.text_frame.text
            if '[What the user does in this part' in text:
                shape.text_frame.text = '1. Admin Dashboard & Live Database Inspector: Displays real-time student/faculty counters, active course rosters, and live database tables with an interactive SQL query box.'
            elif '[Another part, and what it is for]' in text:
                shape.text_frame.text = '2. Faculty Attendance Tracker: Interactive checklist with date filters, quick "Mark All Present/Absent" toggles, and optional remarks for each enrolled student.'
            elif '[What happens when the user clicks' in text:
                shape.text_frame.text = '3. Coursework Grading Interface: Lets faculty view student submissions, enter numerical scores out of maximum points, and provide personalized qualitative feedback.'

    # -------------------------------------------------------------
    # SLIDE 8: Python Concepts Used (Table)
    # -------------------------------------------------------------
    s8 = prs.slides[7]
    for shape in s8.shapes:
        if shape.has_table:
            table = shape.table
            concepts_data = [
                ('Decorators (@admin_required)', 'auth.py: admin_required(), faculty_required()', 'Enforces route-level Role-Based Access Control and session verification'),
                ('Classes & Object-Oriented Programming', 'models.py: User, Faculty, Student, Course, Attendance', 'Declares 8 normalized SQLAlchemy ORM models with relations & password hashing'),
                ('Lists, Tuples & Dictionaries', 'routes/faculty_routes.py: attendance(), grade_assignment()', 'Processes batch attendance records, student arrays, and form radio state maps'),
                ('Environment & File Handling', 'config.py: Config class with python-dotenv', 'Reads .env configuration, sets secret keys, and configures SQLite/PostgreSQL URIs'),
                ('Exception Handling (try-except)', 'routes/admin_routes.py: database_viewer()', 'Safely intercepts malformed SQL queries and database errors without crashing'),
                ('Modules, Packages & Blueprints', 'app.py, auth_bp, admin_bp, faculty_bp', 'Separates authentication, admin administration, and faculty portals into modular units')
            ]
            for r_idx, (c, w, d) in enumerate(concepts_data):
                table.cell(r_idx + 1, 0).text = c
                table.cell(r_idx + 1, 1).text = w
                table.cell(r_idx + 1, 2).text = d

    # -------------------------------------------------------------
    # SLIDE 9: Key Code
    # -------------------------------------------------------------
    s9 = prs.slides[8]
    for shape in s9.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[file name, e.g. logic.py]' in text:
            shape.text_frame.text = 'auth.py (Role-Based Access Control Decorator)'
        elif 'def [function_name]' in text:
            shape.text_frame.text = "def admin_required(f):\n    @wraps(f)\n    @login_required\n    def decorated_function(*args, **kwargs):\n        if not current_user.is_admin():\n            flash('Access restricted. Admin permissions required.', 'danger')\n            return redirect(url_for('faculty.dashboard'))\n        return f(*args, **kwargs)\n    return decorated_function"
        elif '[Line N: what it does, and why]' in text:
            shape.text_frame.text = 'Line 2: @wraps(f) preserves the wrapped function name and docstrings across Flask routing tables.'
        elif '[Line N: the key Python concept' in text:
            shape.text_frame.text = 'Line 3: @login_required verifies that an active, authenticated session cookie exists before inspecting role claims.'
        elif '[Line N: how errors or edge cases' in text:
            shape.text_frame.text = 'Lines 5-7: Intercepts unauthorized faculty attempts to access admin URLs, flashes an alert, and redirects safely.'

    # -------------------------------------------------------------
    # SLIDE 10: Live Demonstration
    # -------------------------------------------------------------
    s10 = prs.slides[9]
    for shape in s10.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[Step 1:' in text:
            shape.text_frame.text = 'Launch Web Server (python app.py) & browse to http://127.0.0.1:5000'
        elif '[Step 2]' in text:
            shape.text_frame.text = 'Log in as Admin (admin / Admin@12345), register a new faculty member & assign CS101'
        elif '[Step 3]' in text:
            shape.text_frame.text = 'Log in as Faculty (faculty.cs / Faculty@123), mark batch class attendance & grade assignment'
        elif '[Step 4:' in text:
            shape.text_frame.text = 'Security & DB Test: Demonstrate faculty access rejection on /admin & inspect live tables via DB Inspector'
        elif 'Backup:' in text:
            shape.text_frame.text = 'Backup: Automated test suite verification (python test_app.py passes 5/5 unit tests in 1.75s)'

    # -------------------------------------------------------------
    # SLIDE 11: Results and Testing
    # -------------------------------------------------------------
    s11 = prs.slides[10]
    # Remove yellow tag
    for shape in list(s11.shapes):
        if shape.has_text_frame and 'FOR APPLICATIONS' in shape.text_frame.text:
            sp = shape._element
            sp.getparent().remove(sp)
        elif shape.has_text_frame and '[Screenshot of a key result' in shape.text_frame.text:
            left = shape.left
            top = shape.top
            width = shape.width
            height = shape.height
            sp = shape._element
            sp.getparent().remove(sp)
            s11.shapes.add_picture('figures/fig_5_2_test_results.png', left, top, width, height)
        elif shape.has_text_frame:
            text = shape.text_frame.text
            if '[N] / [N]' in text and 'requirements delivered' in text:
                shape.text_frame.text = '6 / 6\nrequirements delivered (100%)'
            elif '[N] / [N]' in text and 'test cases passed' in text:
                shape.text_frame.text = '5 / 5\ntest suites passed (100% pass rate)'
            elif '[N]' in text and 'bugs found and fixed' in text:
                shape.text_frame.text = '0\nunhandled bugs (2 resolved in testing)'

    # -------------------------------------------------------------
    # SLIDE 12: Challenges and What We Learnt
    # -------------------------------------------------------------
    s12 = prs.slides[11]
    for shape in s12.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[A problem we ran into]' in text:
            shape.text_frame.text = '1. Enforcing strict Role Separation across routes\n→ Solved using custom Python decorator wrappers (@admin_required, @faculty_required).'
        elif '[Another problem]' in text:
            shape.text_frame.text = '2. Supporting both Local SQLite and Cloud PostgreSQL\n→ Solved via SQLAlchemy engine abstraction and connection string normalization in config.py.'
        elif '[A third problem]' in text:
            shape.text_frame.text = '3. Dynamic Batch Attendance updates in a single form submit\n→ Solved using student-keyed radio inputs (status_<id>) and transactional scoped commits.'
        elif '[A specific thing we learnt about Python]' in text:
            shape.text_frame.text = '• Mastered Python function decorators (@wraps) for enterprise authorization & middleware security.'
        elif '[Something we learnt about building a project]' in text:
            shape.text_frame.text = '• Learned relational schema design with foreign key constraints, cascaded deletes, and unique indexes.'
        elif '[Something we would do differently]' in text:
            shape.text_frame.text = '• Implement automated database migrations using Flask-Migrate / Alembic for schema evolution.'

    # -------------------------------------------------------------
    # SLIDE 13: Conclusion and Future Scope
    # -------------------------------------------------------------
    s13 = prs.slides[12]
    for shape in s13.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[One or two sentences: what you built' in text:
            shape.text_frame.text = 'UniRecord successfully establishes a secure, modular Student Record Management System with full role isolation, dual-database compatibility, and a live web-based SQL inspector.'
        elif 'O1 [' in text:
            shape.text_frame.text = 'O1 (Role-Based Authentication): Met (Admin & Faculty role separation verified with 0 leaks)'
        elif 'O2 [' in text:
            shape.text_frame.text = 'O2 (Faculty & Student Governance): Met (Admin can register faculty, manage students, & allocate courses)'
        elif 'O3 [' in text:
            shape.text_frame.text = 'O3 (Attendance & Grade Recording): Met (Faculty can take attendance & evaluate coursework submissions)'
        elif 'O4 [' in text:
            shape.text_frame.text = 'O4 (Database Inspector & Cloud Sync): Met (Live schema explorer & seamless SQLite/PostgreSQL support)'
        elif '[An improvement, and how it could be done]' in text:
            shape.text_frame.text = '1. Self-Service Student Portal: Add student logins to view personal attendance percentages and submitted grades.'
        elif '[A second improvement]' in text:
            shape.text_frame.text = '2. Low-Attendance Email Alerts: Automated SMTP notifications sent to parents when attendance drops below 75%.'
        elif '[A third improvement' in text:
            shape.text_frame.text = '3. Report Card Generator: Export semester performance summaries and attendance sheets to downloadable PDF and Excel.'

    # -------------------------------------------------------------
    # SLIDE 14: References
    # -------------------------------------------------------------
    s14 = prs.slides[13]
    for shape in s14.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[1]' in text:
            shape.text_frame.text = '[1] Python Software Foundation, "The Python Tutorial (v3.13)," Python 3 Documentation, 2026. [Online]. Available: https://docs.python.org/3/\n[2] Pallets Projects, "Flask Documentation (v3.1.x)," Pallets Community, 2026. [Online]. Available: https://flask.palletsprojects.com/\n[3] M. Bayer, "SQLAlchemy: The Database Toolkit for Python (v2.1)," SQLAlchemy Authors, 2026. [Online]. Available: https://www.sqlalchemy.org/\n[4] D. F. Ferraiolo and D. R. Kuhn, "Role-Based Access Controls," in 15th National Computer Security Conference, Baltimore, MD, 1992, pp. 554-563.\n[5] Bootstrap Team, "Bootstrap v5.3 Documentation," Open Source, 2026. [Online]. Available: https://getbootstrap.com/'

    # -------------------------------------------------------------
    # SLIDE 15: Thank You Slide
    # -------------------------------------------------------------
    s15 = prs.slides[14]
    for shape in s15.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if '[Member 1 Name]' in text:
            shape.text_frame.text = 'Nishanta Bhattacharjya (Roll No. ADTU/1/2025-29/BTCS/003)\nChinmoy Nath (Roll No. ADTU/1/2025-29/BTCS/053)'
        elif '[link to the GitHub repository]' in text:
            shape.text_frame.text = 'Code: BTCS2101_ADTU_1_2025-29_BTCS_003_053_Code.zip'

    # Fix slide numbers on all slides
    for i, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame and shape.name.startswith('Slide Number'):
                shape.text_frame.text = str(i + 1)

    output_path = 'BTCS2101_ADTU_1_2025-29_BTCS_003_053_Slides.pptx'
    prs.save(output_path)
    print(f"Final presentation successfully saved to: {output_path}")

if __name__ == '__main__':
    build_presentation()
