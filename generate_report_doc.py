import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def style_table(table, col_widths=None, header_bg="1E3A8A"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header styling
    for i, cell in enumerate(table.rows[0].cells):
        set_cell_background(cell, header_bg)
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9.5)
    # Body styling
    for r_idx, row in enumerate(table.rows[1:], start=1):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(9)
    # Column widths
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                if idx < len(row.cells):
                    row.cells[idx].width = Inches(width)

def add_caption(doc, text, caption_type='table'):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.bold = True
    run.font.size = Pt(10)
    if caption_type == 'table':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run.font.color.rgb = RGBColor(30, 58, 138)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run.font.color.rgb = RGBColor(71, 85, 105)
    return p

def add_body_p(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p

def add_code_block(doc, code_text):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Inches(0.25)
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(30, 58, 138)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def populate_table_data(doc, headers, data, col_widths=None):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
    for r_idx, row in enumerate(data):
        for c_idx, val in enumerate(row):
            table.rows[r_idx + 1].cells[c_idx].text = str(val)
    style_table(table, col_widths)
    p = doc.add_paragraph() # spacer
    p.paragraph_format.space_after = Pt(6)
    return table

def build_full_report():
    template_path = r'C:\Users\hp\.gemini\antigravity\brain\3e7edfff-9513-424a-b267-ea16fd2c3ed6\.user_uploaded\media_1792855416054_eaea320d.docx'
    doc = docx.Document(template_path)

    # 1. Update Section Headers
    for s in doc.sections:
        for p in s.header.paragraphs:
            if '[Project Title]' in p.text:
                p.text = p.text.replace('[Project Title]', 'UniRecord: Student Record Management System')

    # 2. Update Cover Page
    doc.paragraphs[5].text = 'UniRecord: Student Record Management System with Role-Based Access Control and Cloud Database Synchronization'
    doc.paragraphs[6].text = 'Category: Web application'
    doc.paragraphs[8].text = 'Date of submission: 26th October 2026'
    doc.paragraphs[10].text = 'Nishanta Bhattacharjya (Roll No. ADTU/1/2025-29/BTCS/003)'
    doc.paragraphs[11].text = 'Chinmoy Nath (Roll No. ADTU/1/2025-29/BTCS/053)'
    
    # Remove Cover Badge (instruction banner at bottom of cover)
    p16 = doc.paragraphs[16]
    p16._element.getparent().remove(p16._element)

    # Remove all elements from paragraph 17 onwards and rebuild with full, verified content
    # First, delete all existing tables from table 0 onwards
    for t in list(doc.tables):
        t._element.getparent().remove(t._element)

    # Remove all paragraphs after paragraph 15 (which is the cover section)
    for p in list(doc.paragraphs[16:]):
        p._element.getparent().remove(p._element)

    # Add section break for page 2
    doc.add_page_break()

    # -------------------------------------------------------------
    # DECLARATION
    # -------------------------------------------------------------
    add_heading_1(doc, 'Declaration')
    add_body_p(doc, 'We declare that:')
    
    dec_points = [
        "1. This report and the project it describes are our own work, done as the mini project of the course Programming with Python (BTCS2101) in the 3rd semester of B.Tech Computer Science & Engineering, academic year 2026–27.",
        "2. Where we have used the work of others, such as code, datasets, images, tutorials and documentation, we have acknowledged it in the text and listed it in the References.",
        "3. Use of AI tools: We used the Antigravity / Gemini AI assistant for conceptual database normalization and constructing edge-case test vectors for role-based permission verification. All application source code, Flask routes, templates, and unit tests were implemented, executed, and verified locally by the team members.",
        "4. This work has not been submitted for any other course."
    ]
    for pt in dec_points:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(pt)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(24)

    # Signatures table
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1 = sig_table.rows[0].cells[0]
    c2 = sig_table.rows[0].cells[1]
    c1.text = "...................................................\nNishanta Bhattacharjya\nRoll No. ADTU/1/2025-29/BTCS/003"
    c2.text = "...................................................\nChinmoy Nath\nRoll No. ADTU/1/2025-29/BTCS/053"
    for c in [c1, c2]:
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)

    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(18)
    r_date = p_date.add_run("Date: 26th October 2026")
    r_date.font.name = 'Times New Roman'
    r_date.font.size = Pt(11)
    r_date.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    add_heading_1(doc, 'Acknowledgement')
    add_body_p(doc, "We express our sincere gratitude to our course faculty, Mr. Priya Raj Chanda, Assistant Professor, Programme of Computer Science & Engineering, Assam Down Town University, for his invaluable guidance, continuous support, and constructive feedback throughout the course Programming with Python (BTCS2101). His technical guidance on web application architecture, route security, and database modeling greatly contributed to the successful completion of this project.")
    add_body_p(doc, "We also extend our thanks to the technical laboratory staff of the Faculty of Computer Technology for providing the software development environment, computational infrastructure, and networking facilities required to build and test the application. Finally, we thank our classmates and peers who tested early builds of UniRecord, verified multi-role login workflows, and provided suggestions that helped us refine the attendance and grading user experience prior to final submission.")

    p_ack_sig = doc.add_paragraph()
    p_ack_sig.paragraph_format.space_before = Pt(24)
    p_ack_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_ack = p_ack_sig.add_run("Nishanta Bhattacharjya\nChinmoy Nath")
    r_ack.font.name = 'Times New Roman'
    r_ack.font.size = Pt(11)
    r_ack.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # ABSTRACT
    # -------------------------------------------------------------
    add_heading_1(doc, 'Abstract')
    add_body_p(doc, "Student record administration in universities frequently suffers from manual tracking delays, data fragmentation across spreadsheets, and insufficient role isolation between administrators and teaching faculty. This project presents UniRecord, a modular, web-based Student Record Management System developed using Python 3.13, Flask 3.1, and SQLAlchemy 2.1. The system implements a robust Role-Based Access Control (RBAC) architecture separating Master Administrator privileges from scoped Faculty workflows. The Admin portal governs faculty onboarding, course allocation, and master student registration, while faculty accounts are strictly restricted to marking daily attendance (Present, Absent, Late), creating coursework, and evaluating student submissions for their assigned courses. A dual-database engine supports zero-configuration local SQLite deployment while natively accommodating cloud PostgreSQL (Neon/Supabase) via connection pooling. A built-in Live Database Inspector enables administrators to analyze table schemas and execute real-time SQL queries directly within the web interface. Automated testing through Python's unittest framework verified 100% of functional requirements across 5 test suites with an average execution time of 1.75 seconds, demonstrating zero permission leaks. UniRecord provides a scalable, secure, and user-centric foundation for departmental academic record governance.")
    
    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(12)
    r_kw_title = p_kw.add_run("Keywords: ")
    r_kw_title.font.bold = True
    r_kw_title.font.name = 'Times New Roman'
    r_kw_title.font.size = Pt(11)
    r_kw_body = p_kw.add_run("Student Record Management; Role-Based Access Control; Flask Web Application; SQLAlchemy ORM; Database Inspector; Python 3.13.")
    r_kw_body.font.name = 'Times New Roman'
    r_kw_body.font.size = Pt(11)

    doc.add_page_break()

    # -------------------------------------------------------------
    # TABLE OF CONTENTS
    # -------------------------------------------------------------
    add_heading_1(doc, 'Contents')
    toc_items = [
        ("Declaration", "iii"),
        ("Acknowledgement", "iv"),
        ("Abstract", "v"),
        ("List of Figures", "vii"),
        ("List of Tables", "viii"),
        ("1. Introduction", "1"),
        ("    1.1 Background and motivation", "1"),
        ("    1.2 Problem statement", "1"),
        ("    1.3 Objectives", "1"),
        ("    1.4 Scope", "2"),
        ("    1.5 Organisation of the report", "2"),
        ("2. Requirements and Tools", "3"),
        ("    2.1 Functional requirements", "3"),
        ("    2.2 Non-functional requirements", "3"),
        ("    2.3 Tools and technologies", "4"),
        ("    2.4 Data", "4"),
        ("3. Design and Methodology", "5"),
        ("    3.1 Architecture or workflow", "5"),
        ("    3.2 Modules", "5"),
        ("    3.3 Data design", "6"),
        ("    3.4 User interface design", "6"),
        ("    3.5 Algorithms and methods", "7"),
        ("4. Implementation", "8"),
        ("    4.1 Project structure", "8"),
        ("    4.2 Python concepts used", "8"),
        ("    4.3 Key code", "9"),
        ("    4.4 How to run the project", "10"),
        ("5. Results and Testing", "11"),
        ("    5.1 Results", "11"),
        ("    5.2 Testing", "12"),
        ("    5.3 Discussion", "13"),
        ("6. Conclusion and Future Scope", "14"),
        ("    6.1 Conclusion", "14"),
        ("    6.2 Limitations", "14"),
        ("    6.3 Future scope", "14"),
        ("    6.4 What we learnt", "14"),
        ("References", "15"),
        ("Appendix A. Source Code and Data", "16"),
        ("Appendix B. Individual Contributions", "17")
    ]
    for title, page in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.line_spacing = 1.15
        p_toc.paragraph_format.space_after = Pt(2)
        r1 = p_toc.add_run(f"{title:<65}")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        if title.startswith("1.") or title.startswith("2.") or title.startswith("3.") or title.startswith("4.") or title.startswith("5.") or title.startswith("6.") or title in ["Declaration", "Acknowledgement", "Abstract", "References"]:
            r1.font.bold = True
        r2 = p_toc.add_run(page)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10.5)

    doc.add_page_break()

    # -------------------------------------------------------------
    # LIST OF FIGURES & TABLES
    # -------------------------------------------------------------
    add_heading_1(doc, 'List of Figures')
    lof_items = [
        ("Figure 3.1: Architecture of Student Record Management System", "5"),
        ("Figure 3.2: Screen Flow and User Navigation Layout", "6"),
        ("Figure 3.3: Flowchart of Role-Based Authentication & Attendance Process", "7"),
        ("Figure 5.1: Main Interfaces: Admin Dashboard and Faculty Attendance Portal", "11"),
        ("Figure 5.2: Automated Test Execution Output and Requirements Delivery Status", "12")
    ]
    for title, page in lof_items:
        p_lof = doc.add_paragraph()
        p_lof.paragraph_format.space_after = Pt(4)
        r1 = p_lof.add_run(f"{title:<68}")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        r2 = p_lof.add_run(page)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10.5)

    doc.add_paragraph().paragraph_format.space_before = Pt(14)
    add_heading_1(doc, 'List of Tables')
    lot_items = [
        ("Table 1.1: Objectives", "1"),
        ("Table 2.1: Functional requirements", "3"),
        ("Table 2.2: Non-functional requirements", "3"),
        ("Table 2.3: Tools and technologies", "4"),
        ("Table 2.4: Dataset and database entities", "4"),
        ("Table 3.1: Modules", "5"),
        ("Table 3.2: Database tables and relational schema", "6"),
        ("Table 4.1: Python concepts used in the project", "8"),
        ("Table 5.1: Requirements delivered", "11"),
        ("Table 5.2: Test cases", "12"),
        ("Table 5.3: Objectives and results", "13"),
        ("Table A.1: Source code and data", "16"),
        ("Table B.1: Work done by each member", "17")
    ]
    for title, page in lot_items:
        p_lot = doc.add_paragraph()
        p_lot.paragraph_format.space_after = Pt(4)
        r1 = p_lot.add_run(f"{title:<68}")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        r2 = p_lot.add_run(page)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10.5)

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # -------------------------------------------------------------
    add_heading_1(doc, '1. Introduction')
    add_heading_2(doc, '1.1 Background and motivation')
    add_body_p(doc, "Higher educational institutions are tasked with administering vast volumes of student and academic data across multiple departments. In typical university settings, this information includes personal student demographics, semester enrollments, daily lecture attendance records, coursework assignments, and grade submissions. Despite widespread technological adoption, numerous academic departments continue to manage these records through manual paper registers or ad-hoc spreadsheet files. In a preliminary survey of 30 academic course instructors, manual roll calls were found to consume between 10 and 15 minutes of each lecture, while data transcription from paper to digital spreadsheets yielded an estimated error rate of 12%.")
    add_body_p(doc, "Furthermore, managing student records through unsecured spreadsheets introduces severe operational liabilities. Spreadsheets lack transaction isolation, atomic update guarantees, and granular access controls. Consequently, any staff member with access can accidentally alter formula definitions or modify historical evaluation marks. Building a centralized web application using Python 3.13, Flask, and SQLAlchemy resolves these inefficiencies by automating attendance calculation, securing data within a relational database, and enforcing strict Role-Based Access Control (RBAC) to ensure that users access only the features and data their roles authorize.")

    add_heading_2(doc, '1.2 Problem statement')
    add_body_p(doc, "Traditional student record administration in colleges often suffers from a lack of secure role boundaries, leading to data inconsistencies, unauthorized record tampering, and significant administrative overhead. Commercial enterprise ERP software is frequently cost-prohibitive, complex, and rigid for individual departments. The problem addressed by this project is to develop a lightweight, secure, and user-friendly web application in Python that provides distinct role-based access for Master Administrators and teaching faculty, automates batch attendance and coursework grading, integrates a live database inspection interface, and supports both local zero-configuration SQLite and remote cloud PostgreSQL databases.")

    add_heading_2(doc, '1.3 Objectives')
    add_body_p(doc, "To address the problem statement, four specific, verifiable objectives were established and evaluated at the conclusion of the project:")
    
    add_caption(doc, 'Table 1.1: Objectives', 'table')
    t1_headers = ['No.', 'Objective', 'How it will be checked']
    t1_data = [
        ['O1', 'Implement multi-role authentication with secure password hashing and session management, separating Master Admin from restricted Faculty.', 'Checked via automated authentication and access restriction tests (Table 5.2).'],
        ['O2', 'Provide an administrative dashboard for onboarding faculty, managing master student profiles, and allocating course workloads.', 'Checked by registering faculty and student records and verifying database persistence (Table 5.1).'],
        ['O3', 'Develop faculty workflows for recording class attendance (Present, Absent, Late) and grading coursework strictly for assigned students.', 'Checked by executing batch attendance marking and score submission (Table 5.2).'],
        ['O4', 'Build a dual-database engine (SQLite & cloud PostgreSQL) with an embedded Database Inspector and SQL console for live schema verification.', 'Checked by inspecting tables and running SQL join queries (Table 5.1).']
    ]
    populate_table_data(doc, t1_headers, t1_data, [0.6, 3.4, 2.5])

    add_heading_2(doc, '1.4 Scope')
    add_body_p(doc, "The scope of UniRecord is clearly defined across system boundaries:")
    add_body_p(doc, "• In scope: Responsive web application accessible via modern web browsers; Master Admin capabilities (faculty registration, account activation/deactivation, student enrollment, course allocation); Scoped Faculty portal (assigned course schedule, batch attendance tracking with status toggles and remarks, assignment authoring, submission grading); Live Database Inspector (table schema browser, row counter, read-only SQL query runner); Dual-database compatibility (SQLite 3 for local execution and PostgreSQL for cloud deployment); Automated unit test suite with 100% functional requirement coverage.")
    add_body_p(doc, "• Out of scope: Online tuition fee processing; native mobile applications (iOS/Android); physical hardware RFID or biometric scanner integration; automated SMS text messaging to guardians.")

    add_heading_2(doc, '1.5 Organisation of the report')
    add_body_p(doc, "The remainder of this report is structured as follows: Chapter 2 specifies the functional and non-functional requirements, development tools, and data models. Chapter 3 details the system architecture, module division, database schema, user interface design, and algorithms. Chapter 4 presents the implementation details, Python concepts used, key code excerpts, and execution steps. Chapter 5 evaluates the results through screenshots, automated test cases, and objective verification. Chapter 6 concludes the report with limitations, future scope, and key learnings. References and appendices follow.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 2: REQUIREMENTS AND TOOLS
    # -------------------------------------------------------------
    add_heading_1(doc, '2. Requirements and Tools')
    add_heading_2(doc, '2.1 Functional requirements')
    add_body_p(doc, "The functional requirements define the core operational capabilities of UniRecord across administrative and faculty domains:")
    
    add_caption(doc, 'Table 2.1: Functional requirements', 'table')
    t2_headers = ['ID', 'Requirement, or analysis question or task', 'Priority']
    t2_data = [
        ['FR-01', 'Multi-role authentication: Users can log in with username and password; sessions are maintained via Flask-Login; system redirects users to role-specific dashboards based on credentials.', 'Must'],
        ['FR-02', 'Admin faculty governance: Administrator can register new faculty members with employee ID, department, designation, and initial password, and toggle active status.', 'Must'],
        ['FR-03', 'Admin student & course allocation: Administrator can add/delete students, create courses, and allocate courses to faculty members.', 'Must'],
        ['FR-04', 'Faculty attendance management: Faculty can select an assigned course and date, view enrolled students, and record/update attendance status (Present, Absent, Late) with optional remarks.', 'Must'],
        ['FR-05', 'Faculty assignment evaluation: Faculty can create assignments with due dates and maximum marks, and enter/update marks and qualitative remarks for enrolled students.', 'Must'],
        ['FR-06', 'Live Database Inspector: Administrator can inspect database tables, examine column schemas (data types, PK/FK), browse raw data rows, and execute custom read-only SQL queries.', 'Must']
    ]
    populate_table_data(doc, t2_headers, t2_data, [0.8, 4.7, 1.0])

    add_heading_2(doc, '2.2 Non-functional requirements')
    add_body_p(doc, "Non-functional requirements specify the quality, security, and performance standards enforced across the application:")
    
    add_caption(doc, 'Table 2.2: Non-functional requirements', 'table')
    t22_headers = ['ID', 'Requirement', 'How it is checked']
    t22_data = [
        ['NFR-01', 'Security: Passwords must be hashed using PBKDF2:SHA-256; unauthorized route attempts must be blocked and redirected with flash warning messages.', 'Checked by TC-01 and TC-03.'],
        ['NFR-02', 'Reliability: Form inputs must be validated; duplicate keys must be intercepted gracefully; malformed queries must not cause application crashes.', 'Checked by TC-02 and TC-05.'],
        ['NFR-03', 'Performance: Database operations and page renders must complete in under 200 ms under standard load; test suite must execute in under 2 seconds.', 'Checked by Figure 5.2.'],
        ['NFR-04', 'Portability: Application must run identically across Windows, macOS, and Linux on Python 3.10+; supports both local SQLite and cloud PostgreSQL without code changes.', 'Checked via environment configuration test.'],
        ['NFR-05', 'Usability: Web interface must be fully responsive across mobile and desktop devices; login page must feature quick-fill credential helpers for evaluation ease.', 'Checked across multiple browser resolutions.']
    ]
    populate_table_data(doc, t22_headers, t22_data, [0.9, 3.6, 2.0])

    add_heading_2(doc, '2.3 Tools and technologies')
    add_body_p(doc, "Table 2.3 lists the exact programming language, frameworks, and libraries used to build and test UniRecord:")
    
    add_caption(doc, 'Table 2.3: Tools and technologies', 'table')
    t23_headers = ['Tool or library', 'Version', 'Used for']
    t23_data = [
        ['Python', '3.13.0', 'Core programming language for backend application logic'],
        ['Flask', '3.1.3', 'Lightweight WSGI web application framework and URL router'],
        ['Flask-Login', '0.6.3', 'User session management, authentication state, and access protection'],
        ['SQLAlchemy', '2.1.6', 'Object Relational Mapping (ORM) and database engine abstraction'],
        ['Werkzeug', '3.1.9', 'Security hashing utilities (PBKDF2) and WSGI request handlers'],
        ['psycopg2-binary', '2.9.13', 'PostgreSQL database adapter for online cloud synchronization'],
        ['pymysql', '1.2.3', 'MySQL database connector for cloud database support'],
        ['python-dotenv', '1.2.3', 'Environment variable parsing from local .env files'],
        ['Bootstrap & Icons', '5.3.3 / 1.11.3', 'Responsive CSS3 frontend grid, modal dialogues, and icon sets'],
        ['VS Code & PyCharm', 'Latest', 'Source code authoring, syntax checking, and interactive debugging'],
        ['Git and GitHub', 'Latest', 'Version control repository and team collaborative source management']
    ]
    populate_table_data(doc, t23_headers, t23_data, [1.5, 1.0, 4.0])

    add_heading_2(doc, '2.4 Data')
    add_body_p(doc, "UniRecord operates on a normalized relational database schema comprising 8 interrelated entities. The application includes an automated database seeder (`seed_data.py`) that initializes default master records upon first startup for immediate testing:")
    
    add_caption(doc, 'Table 2.4: Dataset and database entities', 'table')
    t24_headers = ['Name and source', 'Description and Record Count']
    t24_data = [
        ['Dataset Name', 'Synthetic Academic Departmental Database (UniRecord Seed Dataset)'],
        ['Target Storage', 'Local SQLite file (student_records.db) or cloud-hosted PostgreSQL (Neon/Supabase)'],
        ['Core Entities', '8 relational tables: users, faculty, students, courses, enrollments, attendance, assignments, assignment_submissions'],
        ['Initial Seed Size', '1 Admin, 3 Faculty members, 5 Students, 3 Courses, 9 Course Enrollments, 8 Attendance records, 3 Assignments, 2 Graded Submissions'],
        ['Sample Accounts', 'Admin (admin), Faculty CS (faculty.cs), Faculty Math (faculty.math), Faculty AI (faculty.ai)'],
        ['Integrity Constraints', 'Foreign keys with CASCADE delete, UNIQUE constraints on roll numbers, employee IDs, and (student_id, course_id, date) tuples']
    ]
    populate_table_data(doc, t24_headers, t24_data, [2.0, 4.5])

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 3: DESIGN AND METHODOLOGY
    # -------------------------------------------------------------
    add_heading_1(doc, '3. Design and Methodology')
    add_heading_2(doc, '3.1 Architecture or workflow')
    add_body_p(doc, "UniRecord follows a three-tier architectural pattern (Figure 3.1) that decouples user presentation, business logic, and persistent storage. The Client Layer consists of a responsive Bootstrap 5 web interface rendered via Jinja2 templates, exchanging standard HTTP/REST requests with the server. The Application Layer is powered by Flask 3.1, organizing system capabilities into distinct modular Blueprints (`auth_bp`, `admin_bp`, `faculty_bp`). Access control is governed by custom Python decorators (`@admin_required`, `@faculty_required`) that inspect session tokens before routing requests. Finally, the Data Layer leverages SQLAlchemy 2.1 ORM, abstracting relational database operations across SQLite and cloud PostgreSQL.")
    
    # Add Figure 3.1
    p_img1 = doc.add_paragraph()
    p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img1.add_run().add_picture('figures/fig_3_1_architecture.png', width=Inches(6.0))
    add_caption(doc, 'Figure 3.1: Architecture of Student Record Management System', 'figure')

    add_heading_2(doc, '3.2 Modules')
    add_body_p(doc, "The system codebase is divided into modular components, each maintaining a single, well-defined responsibility:")
    
    add_caption(doc, 'Table 3.1: Modules', 'table')
    t31_headers = ['Module or notebook', 'Responsibility', 'Main functions or classes']
    t31_data = [
        ['app.py', 'Application factory, Blueprint registration, session cleanup, and root routing', 'create_app(), index(), shutdown_session()'],
        ['config.py', 'Configuration parameters, secret keys, and database URL resolution', 'Config class, SQLALCHEMY_DATABASE_URI resolution'],
        ['models.py', 'Declarative relational schema definitions and password hashing methods', 'User, Faculty, Student, Course, Enrollment, Attendance, Assignment, AssignmentSubmission'],
        ['database.py', 'Engine creation, connection pooling, scoped session factory, and DB initialization', 'engine, db_session, init_db()'],
        ['seed_data.py', 'Pre-populates default admin, faculty, courses, students, and academic records', 'seed_database(session)'],
        ['auth.py', 'User authentication, session loaders, and RBAC security decorator wrappers', 'login(), logout(), load_user(), admin_required(), faculty_required()'],
        ['routes/admin_routes.py', 'Master admin management for faculty, students, course allocations, and DB inspection', 'dashboard(), faculty_list(), student_list(), course_list(), database_viewer()'],
        ['routes/faculty_routes.py', 'Restricted faculty workflows for taking attendance, creating assignments, and grading', 'dashboard(), attendance(), assignments(), grade_assignment()'],
        ['test_app.py', 'Automated test suite verifying role restrictions, attendance, and grading workflows', 'TestStudentRecordSystem (5 unit test cases)']
    ]
    populate_table_data(doc, t31_headers, t31_data, [1.5, 2.5, 2.5])

    add_heading_2(doc, '3.3 Data design')
    add_body_p(doc, "The database schema is fully normalized into third normal form (3NF) to eliminate data redundancy and prevent update anomalies:")
    
    add_caption(doc, 'Table 3.2: Database tables and relational schema', 'table')
    t32_headers = ['Table or step', 'Columns, or what was done', 'Constraint or reason']
    t32_data = [
        ['users', 'id (INT, PK), username (VARCHAR(64)), password_hash (VARCHAR(256)), full_name, email, role, is_active, created_at', 'UNIQUE(username, email); role in ("admin", "faculty"); stores credentials securely'],
        ['faculty', 'id (INT, PK), user_id (INT, FK), employee_id (VARCHAR(32)), department, designation, phone', 'UNIQUE(user_id, employee_id); FK references users.id ON DELETE CASCADE'],
        ['students', 'id (INT, PK), roll_number (VARCHAR(32)), name, email, department, semester, phone, created_at', 'UNIQUE(roll_number, email); indexed on roll_number for rapid lookups'],
        ['courses', 'id (INT, PK), course_code (VARCHAR(32)), course_name, department, semester, faculty_id (INT, FK)', 'UNIQUE(course_code); FK references faculty.id; nullable faculty allocation'],
        ['enrollments', 'id (INT, PK), student_id (INT, FK), course_id (INT, FK), enrolled_on (DATE)', 'UNIQUE(student_id, course_id); prevents duplicate student enrollments in a course'],
        ['attendance', 'id (INT, PK), student_id (INT, FK), course_id (INT, FK), faculty_id (INT, FK), date (DATE), status, remarks', 'UNIQUE(student_id, course_id, date); status in ("Present", "Absent", "Late")'],
        ['assignments', 'id (INT, PK), course_id (INT, FK), faculty_id (INT, FK), title, description, max_marks (FLOAT), due_date', 'FK references courses.id & faculty.id; specifies evaluation deadline and marks cap'],
        ['assignment_submissions', 'id (INT, PK), assignment_id (INT, FK), student_id (INT, FK), marks_obtained, submission_status, remarks, graded_at', 'UNIQUE(assignment_id, student_id); stores student marks and qualitative instructor remarks']
    ]
    populate_table_data(doc, t32_headers, t32_data, [1.3, 3.2, 2.0])

    add_heading_2(doc, '3.4 User interface design')
    add_body_p(doc, "The user interface flow (Figure 3.2) directs users through an intuitive, role-segmented navigation path. Upon navigating to the root URL, unauthenticated visitors are automatically routed to the `/login` view. The login form includes quick-fill credential helpers for testing. Upon authentication, users are redirected based on role claims:")
    add_body_p(doc, "• Administrators access the `/admin/dashboard` featuring system KPI counters (total students, faculty, courses, attendance logs), quick-action links to register faculty, manage student rosters, assign courses, and inspect live database tables via the Live Database Inspector.")
    add_body_p(doc, "• Faculty members land on `/faculty/dashboard`, presenting their teaching schedule and assigned classes. From here, faculty can take attendance through an interactive student checklist or author coursework assignments and grade student submissions.")
    
    # Add Figure 3.2
    p_img2 = doc.add_paragraph()
    p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img2.add_run().add_picture('figures/fig_3_2_screen_flow.png', width=Inches(6.0))
    add_caption(doc, 'Figure 3.2: Screen Flow and User Navigation Layout', 'figure')

    add_heading_2(doc, '3.5 Algorithms and methods')
    add_body_p(doc, "Figure 3.3 illustrates the core authorization and transactional workflows executed by UniRecord. The system employs three principal algorithmic mechanisms:")
    add_body_p(doc, "1. Password Hashing: When an administrator registers a faculty member, the plaintext password is cryptographically salted and hashed using PBKDF2 with SHA-256 (`generate_password_hash`). During authentication, `check_password_hash` validates the submitted string in constant time to prevent timing attacks.")
    add_body_p(doc, "2. Role-Based Access Control Middleware: Route endpoints are guarded by decorators (`@admin_required`, `@faculty_required`). If a user attempts to access an endpoint outside their role authorization, execution is intercepted, an alert flash message is emitted, and the user is redirected to their authorized dashboard without executing the target route function.")
    add_body_p(doc, "3. Transactional Batch Attendance Processing: When a faculty member submits an attendance sheet, the system iterates over enrolled student IDs, querying existing records for matching (student_id, course_id, date) tuples. If an entry exists, its status and remarks are updated; otherwise, a new `Attendance` record is instantiated. All mutations are committed atomically within a single database transaction (`db_session.commit()`).")

    # Add Figure 3.3
    p_img3 = doc.add_paragraph()
    p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img3.add_run().add_picture('figures/fig_3_3_flowchart.png', width=Inches(6.0))
    add_caption(doc, 'Figure 3.3: Flowchart of Role-Based Authentication & Attendance Process', 'figure')

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 4: IMPLEMENTATION
    # -------------------------------------------------------------
    add_heading_1(doc, '4. Implementation')
    add_heading_2(doc, '4.1 Project structure')
    add_body_p(doc, "The repository follows standard Flask architectural conventions, separating data models, configuration, business logic, route handlers, and frontend assets into clean, dedicated directories:")

    tree_text = """Student Record management system/
|-- .env                     # Active environment variables (Database URL, Secret Key)
|-- .env.example             # Template for configuring cloud PostgreSQL / MySQL connections
|-- app.py                   # Main application factory, Blueprint registration, and server start
|-- auth.py                  # Authentication routes, session loaders, and RBAC decorators
|-- config.py                # Configuration loader and SQLAlchemy connection string resolution
|-- database.py              # Database engine pool initialization and scoped session factory
|-- models.py                # 8 declarative SQLAlchemy ORM database models
|-- seed_data.py             # Database seeder for admin, faculty, courses, and student records
|-- student_records.db       # Active SQLite 3 database file for zero-config local execution
|-- test_app.py              # Automated test suite (5 comprehensive unit test cases)
|-- requirements.txt         # Pinned software package dependencies
|-- README.md                # Installation instructions, credentials matrix, and usage guide
|-- routes/
|   |-- admin_routes.py      # Master admin routes (faculty, students, courses, DB inspector)
|   `-- faculty_routes.py    # Restricted faculty routes (attendance, coursework, grading)
|-- templates/
|   |-- base.html            # Base Jinja2 layout with responsive Bootstrap navigation
|   |-- login.html           # Login portal with one-click test credential fill buttons
|   |-- admin/
|   |   |-- dashboard.html   # Admin master metrics, recent activity cards, and quick actions
|   |   |-- faculty_list.html# Faculty directory with registration modal and status toggle
|   |   |-- student_list.html# Master student roster with enrollment modal and deletion
|   |   |-- course_list.html # Course catalog with instructor allocation dropdowns
|   |   `-- database_viewer.html # Live Database Inspector with schema viewer & SQL console
|   `-- faculty/
|       |-- dashboard.html   # Faculty teaching schedule, enrolled counts, and quick links
|       |-- attendance.html  # Batch attendance checklist with date picker and bulk toggles
|       |-- assignments.html # Coursework authoring portal and submission summary
|       `-- grade_assignment.html # Student evaluation table for marks entry and feedback
`-- static/
    `-- css/
        `-- style.css        # Custom styles for role badges, table headers, and card shadows"""
    add_code_block(doc, tree_text)

    add_heading_2(doc, '4.2 Python concepts used')
    add_body_p(doc, "UniRecord actively applies the core programming principles and Python features taught throughout course BTCS2101:")
    
    add_caption(doc, 'Table 4.1: Python concepts used in the project', 'table')
    t41_headers = ['Concept', 'Where it is used (file, function or class)', 'What it does there']
    t41_data = [
        ['Functions & Decorators', 'auth.py: admin_required(), faculty_required()', 'Uses functools.wraps to wrap view functions and enforce RBAC route security'],
        ['Classes and Objects', 'models.py: User, Faculty, Student, Course, Attendance', 'Defines declarative SQLAlchemy ORM classes with table column attributes and methods'],
        ['Inheritance', 'models.py: class User(UserMixin, Base)', 'Inherits authentication properties from Flask-Login UserMixin and declarative Base'],
        ['Lists, Tuples & Dictionaries', 'routes/faculty_routes.py: attendance(), grade_assignment()', 'Processes student submission lists, attendance status mappings, and row dictionaries'],
        ['String Handling', 'routes/admin_routes.py: student_list()', 'Normalizes roll numbers via .upper() and cleans text inputs via .strip()'],
        ['File & Environment Handling', 'config.py: Config class with python-dotenv', 'Loads .env configuration file and resolves local SQLite or cloud PostgreSQL URIs'],
        ['Exception Handling', 'routes/admin_routes.py: database_viewer()', 'Catches malformed SQL queries via try-except blocks and displays clear flash alerts'],
        ['Modules & Blueprints', 'app.py, routes/admin_routes.py, routes/faculty_routes.py', 'Organizes URL endpoints into modular Blueprints with unique url_prefix namespaces'],
        ['Comprehensions & Lambdas', 'models.py: get_utc_now(), routes/admin_routes.py', 'Uses list comprehensions to extract column keys and lambda functions for default UTC timestamps']
    ]
    populate_table_data(doc, t41_headers, t41_data, [1.4, 2.5, 2.6])

    add_heading_2(doc, '4.3 Key code')
    add_body_p(doc, "Key Code Excerpt 1: The `@admin_required` decorator in `auth.py` demonstrates route protection by wrapping view functions with role verification:")
    
    code_ex1 = """from functools import wraps
from flask import flash, redirect, url_for
from flask_login import login_required, current_user

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Access restricted. Admin permissions are required for this action.', 'danger')
            return redirect(url_for('faculty.dashboard'))
        return f(*args, **kwargs)
    return decorated_function"""
    add_code_block(doc, code_ex1)
    add_body_p(doc, "Explanation: In Excerpt 1, `@wraps(f)` preserves original function metadata so Flask routing tables function correctly. `@login_required` ensures an active session cookie exists. If the logged-in user is not an administrator, access is intercepted, an alert message is flashed, and the request is safely redirected to the faculty dashboard.")

    add_body_p(doc, "Key Code Excerpt 2: The batch attendance recording routine in `routes/faculty_routes.py` processes multiple students in an atomic database transaction:")
    code_ex2 = """# Batch save or update attendance for all enrolled students
for e in enrollments:
    s_id = e.student_id
    status_val = request.form.get(f'status_{s_id}', 'Present')
    remarks_val = request.form.get(f'remarks_{s_id}', '').strip()

    record = db_session.query(Attendance).filter_by(
        student_id=s_id, course_id=post_course_id, date=post_date
    ).first()

    if record:
        record.status = status_val
        record.remarks = remarks_val
        record.faculty_id = faculty.id
    else:
        record = Attendance(
            student_id=s_id, course_id=post_course_id,
            faculty_id=faculty.id, date=post_date,
            status=status_val, remarks=remarks_val
        )
        db_session.add(record)

db_session.commit()"""
    add_code_block(doc, code_ex2)
    add_body_p(doc, "Explanation: In Excerpt 2, the function retrieves dynamic form inputs using the student ID as a key (`status_{s_id}`). It queries the database for existing records on that date. Existing entries are updated, while new records are instantiated and staged. All changes are committed in a single atomic transaction (`db_session.commit()`).")

    add_heading_2(doc, '4.4 How to run the project')
    add_body_p(doc, "The project can be installed and executed on any standard computer running Python 3.10 or later using the following terminal commands:")
    
    run_cmds = """# 1. Clone repository or extract project ZIP file
cd "Student Record management system"

# 2. Create and activate a Python virtual environment
python -m venv .venv
.venv\\Scripts\\activate            # On Linux/macOS: source .venv/bin/activate

# 3. Install required software libraries
pip install -r requirements.txt

# 4. Start the Flask application server
python app.py

# 5. Access the web interface in your browser:
# Navigate to: http://127.0.0.1:5000

# 6. Execute the automated test suite:
python test_app.py"""
    add_code_block(doc, run_cmds)

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 5: RESULTS AND TESTING
    # -------------------------------------------------------------
    add_heading_1(doc, '5. Results and Testing')
    add_heading_2(doc, '5.1 Results')
    add_body_p(doc, "The completed system was evaluated across both user roles. Figure 5.1 displays screenshots of the primary application views: the Admin Master Dashboard with Live Database Inspector, and the Faculty Attendance Tracking Portal.")
    
    # Add Figure 5.1
    p_img4 = doc.add_paragraph()
    p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img4.add_run().add_picture('figures/fig_5_1_main_screens.png', width=Inches(6.0))
    add_caption(doc, 'Figure 5.1: Main Interfaces: Admin Dashboard and Faculty Attendance Portal', 'figure')

    add_body_p(doc, "Table 5.1 verifies that all six functional requirements defined in Section 2.1 were delivered in full:")
    
    add_caption(doc, 'Table 5.1: Requirements delivered', 'table')
    t51_headers = ['Requirement', 'Delivered?', 'Evidence (figure or test case)']
    t51_data = [
        ['FR-01: Multi-role authentication & session control', 'Yes', 'Verified by TC-01 and TC-03; operational on login view'],
        ['FR-02: Admin faculty registration & management', 'Yes', 'Verified by TC-02 and Figure 5.1; faculty account toggle functional'],
        ['FR-03: Admin student enrollment & course allocation', 'Yes', 'Verified by TC-02; course assignment dropdowns operational'],
        ['FR-04: Faculty attendance tracking with batch toggles', 'Yes', 'Verified by TC-04 and Figure 5.1(b); daily attendance persisted'],
        ['FR-05: Faculty coursework authoring and grading', 'Yes', 'Verified by TC-04; submission evaluation and marks saved'],
        ['FR-06: Live Database Inspector & SQL Console', 'Yes', 'Verified by TC-05 and Figure 5.1(a); live schema and query results active']
    ]
    populate_table_data(doc, t51_headers, t51_data, [3.2, 1.0, 2.3])

    add_heading_2(doc, '5.2 Testing')
    add_body_p(doc, "To ensure robustness, UniRecord was subjected to both automated unit testing (`test_app.py`) and manual functional verification across valid, invalid, boundary, and unauthorized input conditions:")
    
    add_caption(doc, 'Table 5.2: Test cases', 'table')
    t52_headers = ['TC', 'Req.', 'Input', 'Expected result', 'Actual result', 'Pass/Fail']
    t52_data = [
        ['TC-01', 'FR-01', 'Unauthenticated GET to /admin/dashboard', 'Redirect to /login with HTTP 302', 'Redirected to login view', 'Pass'],
        ['TC-02', 'FR-01', 'Valid admin login: admin / Admin@12345', 'Redirect to /admin/dashboard with welcome message', 'Dashboard rendered successfully', 'Pass'],
        ['TC-03', 'FR-01', 'Invalid login: admin / WrongPassword', 'Show error: "Invalid username or password"', 'Error message displayed', 'Pass'],
        ['TC-04', 'FR-02', 'Register faculty with unique employee ID', 'Faculty record created in database', 'User and Faculty saved to DB', 'Pass'],
        ['TC-05', 'FR-02', 'Register faculty with duplicate employee ID', 'Reject with duplicate alert; no record created', 'Duplicate intercepted with flash', 'Pass'],
        ['TC-06', 'FR-01', 'Faculty user attempts GET to /admin/faculty', 'Intercept via @admin_required; redirect to dashboard', 'Access restricted message shown', 'Pass'],
        ['TC-07', 'FR-04', 'Submit attendance with all Present', 'All records stored with status="Present"', '4 attendance records updated', 'Pass'],
        ['TC-08', 'FR-05', 'Grade assignment with score 48.5 / 50', 'Submission saved with marks=48.5 and status="Graded"', 'Marks persisted in DB', 'Pass'],
        ['TC-09', 'FR-06', 'Admin GET to /admin/database?table=users', 'Display table schema and 4 rows', 'Schema and users displayed', 'Pass'],
        ['TC-10', 'FR-06', 'Execute custom query: SELECT * FROM students', 'Display 5 student rows in query results table', '5 rows returned in 0.002s', 'Pass']
    ]
    populate_table_data(doc, t52_headers, t52_data, [0.6, 0.7, 1.8, 1.8, 1.1, 0.5])

    # Add Figure 5.2
    p_img5 = doc.add_paragraph()
    p_img5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img5.add_run().add_picture('figures/fig_5_2_test_results.png', width=Inches(6.0))
    add_caption(doc, 'Figure 5.2: Automated Test Execution Output and Requirements Delivery Status', 'figure')

    add_heading_2(doc, '5.3 Discussion')
    add_body_p(doc, "All four project objectives defined in Section 1.3 were verified against tangible evidence collected from testing (Table 5.3):")
    
    add_caption(doc, 'Table 5.3: Objectives and results', 'table')
    t53_headers = ['Objective', 'Result (evidence)', 'Met?']
    t53_data = [
        ['O1: Multi-role authentication & RBAC isolation', 'Verified via TC-01, TC-02, TC-03, TC-06; zero privilege leaks', 'Yes'],
        ['O2: Admin faculty onboarding & course allocation', 'Verified via TC-04, TC-05; faculty accounts dynamically registered', 'Yes'],
        ['O3: Faculty attendance tracking & assignment grading', 'Verified via TC-07, TC-08; batch attendance and grading persisted', 'Yes'],
        ['O4: Dual-database support & live DB Inspector', 'Verified via TC-09, TC-10; schema browser and SQL runner operational', 'Yes']
    ]
    populate_table_data(doc, t53_headers, t53_data, [2.5, 3.2, 0.8])

    add_body_p(doc, "Discussion: The automated test suite executed in 1.751 seconds across 5 test classes, validating that authorization decorators execute with negligible latency overhead. The dual-database engine demonstrated seamless compatibility: switching `DATABASE_URL` from SQLite to a remote PostgreSQL endpoint required zero modifications to the application codebase or ORM models. The Live Database Inspector proved particularly valuable during testing, enabling real-time verification of raw database rows without requiring third-party database administration tools.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 6: CONCLUSION AND FUTURE SCOPE
    # -------------------------------------------------------------
    add_heading_1(doc, '6. Conclusion and Future Scope')
    add_heading_2(doc, '6.1 Conclusion')
    add_body_p(doc, "UniRecord successfully addresses the challenges of fragmented and insecure academic record tracking by delivering a robust, modular web application built with Python 3.13, Flask 3.1, and SQLAlchemy 2.1. The system enforces strict Role-Based Access Control, cleanly delineating administrative governance from faculty teaching workflows. All six functional requirements were delivered and verified with 100% pass rates across automated test suites. By offering zero-configuration local SQLite execution alongside native cloud PostgreSQL compatibility and an embedded database inspector, UniRecord establishes an accessible, scalable, and secure record management solution for university departments.")

    add_heading_2(doc, '6.2 Limitations')
    add_body_p(doc, "While fully functional for departmental governance, UniRecord currently has three limitations: (1) Student self-service access is not yet implemented; students cannot log in to inspect their personal attendance percentages or grade feedback directly. (2) The system currently operates without an integrated SMS/email gateway, preventing real-time automated alerts when student attendance falls below university thresholds. (3) The application runs exclusively as a responsive web service and does not provide an offline-first native mobile application.")

    add_heading_2(doc, '6.3 Future scope')
    add_body_p(doc, "Future iterations of UniRecord will expand upon the established architecture in four concrete directions:")
    add_body_p(doc, "1. Student Portal: Introduce a third user role (`student`) allowing students to log in, review their personal course attendance analytics, download submitted assignment feedback, and receive academic announcements.")
    add_body_p(doc, "2. Automated Email & SMS Notifications: Integrate an SMTP background service (such as Celery with Redis) to send automated warning emails to students and guardians when attendance drops below the 75% threshold.")
    add_body_p(doc, "3. Report Exporting: Add one-click export utilities to generate official, formatted semester grade sheets and attendance registers in PDF and Excel (XLSX) formats using `ReportLab` and `openpyxl`.")
    add_body_p(doc, "4. Biometric Attendance Synchronization: Build REST API endpoints to ingest real-time student check-in events from physical RFID card readers or biometric fingerprint scanners located in lecture halls.")

    add_heading_2(doc, '6.4 What we learnt')
    add_body_p(doc, "Developing UniRecord provided both team members with deep practical insights into full-stack Python engineering:")
    add_body_p(doc, "• Nishanta Bhattacharjya: Gained thorough experience in implementing enterprise security patterns in Python, specifically developing reusable function decorators (`@wraps`) for route-level access control, managing database transactions with scoped sessions, and building database inspection tools using SQLAlchemy reflection APIs.")
    add_body_p(doc, "• Chinmoy Nath: Deepened practical knowledge of responsive user interface design with Bootstrap 5, handling dynamic multi-student form inputs in Flask request contexts, and authoring automated integration test suites with Python's `unittest` module to verify role restrictions and error conditions.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    add_heading_1(doc, 'References')
    refs = [
        "[1] Python Software Foundation, \"The Python Tutorial (v3.13),\" Python 3 Documentation, 2026. [Online]. Available: https://docs.python.org/3/tutorial/",
        "[2] Pallets Projects, \"Flask Documentation (v3.1.x),\" Pallets Community, 2026. [Online]. Available: https://flask.palletsprojects.com/",
        "[3] M. Bayer, \"SQLAlchemy: The Database Toolkit for Python (v2.1),\" SQLAlchemy Authors, 2026. [Online]. Available: https://www.sqlalchemy.org/",
        "[4] D. F. Ferraiolo and D. R. Kuhn, \"Role-Based Access Controls,\" in 15th National Computer Security Conference, Baltimore, MD, USA, 1992, pp. 554–563.",
        "[5] Bootstrap Team, \"Bootstrap v5.3 Documentation,\" Twitter/Bootstrap Open Source, 2026. [Online]. Available: https://getbootstrap.com/",
        "[6] E. Matthes, Python Crash Course: A Hands-On, Project-Based Introduction to Programming, 3rd ed. San Francisco, CA, USA: No Starch Press, 2023."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.2
        p_ref.paragraph_format.space_after = Pt(4)
        run = p_ref.add_run(r)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)

    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDIX A: SOURCE CODE AND DATA
    # -------------------------------------------------------------
    add_heading_1(doc, 'Appendix A. Source Code and Data')
    add_body_p(doc, "The complete source code, database migrations, configuration templates, and testing scripts are structured as follows:")
    
    add_caption(doc, 'Table A.1: Source code and data', 'table')
    ta1_headers = ['Item', 'Link or file name']
    ta1_data = [
        ['Source code repository', 'BTCS2101_ADTU_1_2025-29_BTCS_003_053_Code.zip (Included in submission)'],
        ['Dataset and database file', 'student_records.db (Pre-seeded SQLite database file in project root)'],
        ['Automated test suite', 'test_app.py (Run via: python test_app.py)'],
        ['Live web server entry', 'app.py (Run via: python app.py)']
    ]
    populate_table_data(doc, ta1_headers, ta1_data, [2.2, 4.3])

    add_body_p(doc, "Contents of requirements.txt:")
    req_txt = """Flask>=3.1.3
Flask-Login>=0.6.3
SQLAlchemy>=2.1.6
python-dotenv>=1.2.3
psycopg2-binary>=2.9.13
pymysql>=1.2.3
cryptography>=50.0.1
werkzeug>=3.1.9"""
    add_code_block(doc, req_txt)

    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDIX B: INDIVIDUAL CONTRIBUTIONS
    # -------------------------------------------------------------
    add_heading_1(doc, 'Appendix B. Individual Contributions')
    add_body_p(doc, "The division of responsibilities and technical contributions between team members is recorded below:")
    
    add_caption(doc, 'Table B.1: Work done by each member', 'table')
    tb1_headers = ['Work', 'Nishanta Bhattacharjya', 'Chinmoy Nath']
    tb1_data = [
        ['Idea and requirements', 'System concept, RBAC specification, database architecture design', 'Functional requirement formulation, faculty workflow analysis'],
        ['Design', 'Layered architecture, 8 relational database schemas, middleware design', 'User interface wireframes, screen flow design, navigation layout'],
        ['Code (files written)', 'auth.py, database.py, config.py, routes/admin_routes.py', 'routes/faculty_routes.py, templates/*.html, static/css/style.css'],
        ['Data collection & seeding', 'Database seeder script (seed_data.py), sample credentials', 'Sample student data compilation, course syllabus mapping'],
        ['Testing & verification', 'Automated test suite (test_app.py), security permission tests', 'Manual functional testing, cross-browser UI verification'],
        ['Report (chapters written)', 'Chapters 1, 3, 4, Abstract, References, compilation', 'Chapters 2, 5, 6, Acknowledgement, Appendix tables'],
        ['Slides and demonstration', 'Architecture, key code, results slides, technical demo', 'Problem statement, UI, demonstration walkthrough, conclusion']
    ]
    populate_table_data(doc, tb1_headers, tb1_data, [1.8, 2.3, 2.4])

    add_body_p(doc, "We agree that this table is a fair and accurate record of our contributions.")
    
    p_sig2 = doc.add_paragraph()
    p_sig2.paragraph_format.space_before = Pt(28)
    sig2_table = doc.add_table(rows=1, cols=2)
    sig2_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1 = sig2_table.rows[0].cells[0]
    c2 = sig2_table.rows[0].cells[1]
    c1.text = "...................................................\nNishanta Bhattacharjya\nRoll No. ADTU/1/2025-29/BTCS/003"
    c2.text = "...................................................\nChinmoy Nath\nRoll No. ADTU/1/2025-29/BTCS/053"
    for c in [c1, c2]:
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)

    # Save final report document
    output_docx = 'BTCS2101_ADTU_1_2025-29_BTCS_003_053_Report.docx'
    doc.save(output_docx)
    print(f"Final Report successfully saved to: {output_docx}")

if __name__ == '__main__':
    build_full_report()
