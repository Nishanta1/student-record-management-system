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

def style_table(table, col_widths=None, header_bg="2563EB"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header styling
    for i, cell in enumerate(table.rows[0].cells):
        set_cell_background(cell, header_bg)
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
    # Body styling
    for r_idx, row in enumerate(table.rows[1:], start=1):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(9.5)
    # Column widths if provided
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                if idx < len(row.cells):
                    row.cells[idx].width = Inches(width)

def build_report():
    template_path = r'C:\Users\hp\.gemini\antigravity\brain\3e7edfff-9513-424a-b267-ea16fd2c3ed6\.user_uploaded\media_1792855416054_eaea320d.docx'
    doc = docx.Document(template_path)

    # 1. Update Headers across all sections
    for s in doc.sections:
        for p in s.header.paragraphs:
            if '[Project Title]' in p.text:
                p.text = p.text.replace('[Project Title]', 'UniRecord: Student Record Management System')

    # 2. Update Cover Page (Paragraphs 0 to 16)
    doc.paragraphs[5].text = 'UniRecord: Student Record Management System with Role-Based Access Control and Cloud Database Synchronization'
    doc.paragraphs[6].text = 'Category: Web application'
    doc.paragraphs[8].text = 'Date of submission: 26th October 2026'
    doc.paragraphs[10].text = 'Nishanta Bhattacharjya (Roll No. ADTU/1/2025-29/BTCS/003)'
    doc.paragraphs[11].text = 'Chinmoy Nath (Roll No. ADTU/1/2025-29/BTCS/053)'
    
    # Remove Cover Badge (instruction banner at bottom of cover)
    p16 = doc.paragraphs[16]
    p16._element.getparent().remove(p16._element)

    # 3. Remove "How to use this format" section and its two tables (Table 0 and Table 1)
    # Remove Table 0 and Table 1 from template
    t0 = doc.tables[0]._element
    t0.getparent().remove(t0)
    t1 = doc.tables[0]._element
    t1.getparent().remove(t1)

    # Remove the "How to use this format" paragraph
    for p in list(doc.paragraphs):
        if 'How to use this format' in p.text:
            p._element.getparent().remove(p._element)
            break

    # 4. Remove all guidance and example paragraphs
    for p in list(doc.paragraphs):
        if p.style.name in ['Guidance', 'Example']:
            p._element.getparent().remove(p._element)

    # 5. Remove placeholder figure boxes
    for p in list(doc.paragraphs):
        if '[Insert your figure here' in p.text or 'diagram or screenshot, at most the page width' in p.text:
            p._element.getparent().remove(p._element)

    # Save intermediate to inspect cleaned state
    doc.save('BTCS2101_ADTU_1_2025-29_BTCS_003_053_Report.docx')
    print("Intermediate clean completed successfully!")

if __name__ == '__main__':
    build_report()
