from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
from io import BytesIO


# =============================
# HELPER: REMOVE SPACING
# =============================
def set_paragraph_spacing(paragraph, before=5, after=5, line=1):
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = line


def generate_resume_docx(resume):
    doc = Document()

    # =============================
    # GLOBAL STYLE FIX (IMPORTANT)
    # =============================
    style = doc.styles['Normal']
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)

    # =============================
    # PAGE MARGINS
    # =============================
    section = doc.sections[0]
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    # =============================
    # HEADER
    # =============================
    table = doc.add_table(rows=1, cols=2)
    table.autofit = True

    left = table.rows[0].cells[0]
    right = table.rows[0].cells[1]

    # LEFT
    p = left.paragraphs[0]
    run = p.add_run(resume.name)
    run.bold = True
    run.font.size = Pt(20)
    set_paragraph_spacing(p)

    p = left.add_paragraph(resume.position)
    p.runs[0].font.size = Pt(12)
    set_paragraph_spacing(p)

    # RIGHT
    p = right.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    current_date = datetime.now().strftime("%d %b %Y")
    p.add_run(f"Date: {current_date}")
    set_paragraph_spacing(p)

    # =============================
    # CONTACT
    # =============================
    p = doc.add_paragraph()
    p.add_run("Phone: ").bold = True
    p.add_run(resume.phone)
    set_paragraph_spacing(p)

    p = doc.add_paragraph()
    p.add_run("Email: ").bold = True
    p.add_run(resume.email)
    set_paragraph_spacing(p)

    p = doc.add_paragraph()
    p.add_run("Address: ").bold = True
    p.add_run(resume.address)
    set_paragraph_spacing(p)

    if getattr(resume, "website", ""):
        p = doc.add_paragraph()
        p.add_run("Website: ").bold = True
        p.add_run(resume.website)
        set_paragraph_spacing(p)

    # =============================
    # SUMMARY
    # =============================
    if resume.summary:
        p = doc.add_paragraph("\nProfessional Summary")
        run = p.runs[0]
        run.bold = True
        run.font.size = Pt(14)
        set_paragraph_spacing(p, before=6, after=2)
        p = doc.add_paragraph(resume.summary)
        set_paragraph_spacing(p)

    # =============================
    # SKILLS
    # =============================
    skills = []
    for category in resume.skill_categories.all():
        for skill in category.skills.all():
            skills.append(skill.name)

    if skills:
        p = doc.add_paragraph("\nSkills")
        run = p.runs[0]
        run.bold = True
        run.font.size = Pt(14)
        set_paragraph_spacing(p, before=6, after=2)

        table = doc.add_table(rows=1, cols=3)

        col_data = [
            skills[0::3],
            skills[1::3],
            skills[2::3],
        ]

        for i, col in enumerate(col_data):
            cell = table.rows[0].cells[i]
            for skill in col:
                p = cell.add_paragraph(f"• {skill}")
                set_paragraph_spacing(p, before=0, after=0)

        # remove hidden spacing inside table
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    set_paragraph_spacing(paragraph, 0, 0)

    # =============================
    # EXPERIENCE
    # =============================
    if resume.journey.all():
        p = doc.add_paragraph("\nWork Experience")
        run = p.runs[0]
        run.bold = True
        run.font.size = Pt(14)
        set_paragraph_spacing(p, before=6, after=2)

        for journey in resume.journey.all():
            for item in journey.excellences.all():
                p = doc.add_paragraph(item.title)
                p.runs[0].bold = True
                set_paragraph_spacing(p)

                p = doc.add_paragraph(f"{item.company} | {item.date_range}")
                set_paragraph_spacing(p)

                p = doc.add_paragraph(item.description)
                set_paragraph_spacing(p)

    # =============================
    # CERTIFICATIONS
    # =============================
    certs = []
    for profession in resume.professions.all():
        for cert in profession.certifications.all():
            if cert.is_active:
                certs.append(cert.title)

    if certs:
        p = doc.add_paragraph("\nCertifications")
        run = p.runs[0]
        run.bold = True
        run.font.size = Pt(14)
        set_paragraph_spacing(p, before=6, after=2)

        table = doc.add_table(rows=1, cols=2)

        col_data = [
            certs[0::2],
            certs[1::2],
        ]

        for i, col in enumerate(col_data):
            cell = table.rows[0].cells[i]
            for cert in col:
                p = cell.add_paragraph(f"• {cert}")
                set_paragraph_spacing(p)

        # remove spacing inside table
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    set_paragraph_spacing(paragraph, 0, 0)

    # =============================
    # EDUCATION
    # =============================
    if resume.journeys.all():
        p = doc.add_paragraph("\nEducation")
        run = p.runs[0]
        run.bold = True
        run.font.size = Pt(14)
        set_paragraph_spacing(p, before=6, after=2)

        for item in resume.journeys.all():
            if item.is_active:
                p = doc.add_paragraph(f"{item.description} ({item.year})")
                set_paragraph_spacing(p)

    # =============================
    # SAVE
    # =============================
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer