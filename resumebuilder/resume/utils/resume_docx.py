from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
from io import BytesIO


def generate_resume_docx(resume):
    doc = Document()

    # =============================
    # PAGE MARGINS
    # =============================
    section = doc.sections[0]
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    # =============================
    # HEADER (NAME + TITLE + DATE)
    # =============================
    header_table = doc.add_table(rows=1, cols=2)
    header_table.autofit = True

    # LEFT SIDE
    left_cell = header_table.rows[0].cells[0]
    p = left_cell.paragraphs[0]
    run = p.add_run(resume.name)
    run.bold = True
    run.font.size = Pt(20)

    p = left_cell.add_paragraph()
    p.add_run(resume.position).font.size = Pt(12)

    # RIGHT SIDE (DATE)
    right_cell = header_table.rows[0].cells[1]
    p = right_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    current_date = datetime.now().strftime("%d %b %Y")
    p.add_run(f"Date: {current_date}")

    # =============================
    # CONTACT
    # =============================
    contact = doc.add_paragraph()
    contact.add_run("Phone: ").bold = True
    contact.add_run(resume.phone + "\n")

    contact.add_run("Email: ").bold = True
    contact.add_run(resume.email + "\n")

    contact.add_run("Address: ").bold = True
    contact.add_run(resume.address + "\n")

    contact.add_run("Website: ").bold = True
    contact.add_run(getattr(resume, "website", ""))

    # =============================
    # SUMMARY
    # =============================
    if resume.summary:
        p = doc.add_paragraph()
        run = p.add_run("\nProfessional Summary\n")
        run.bold = True
        run.font.size = Pt(14)

        doc.add_paragraph(resume.summary)

    # =============================
    # SKILLS (3 COLUMN TABLE)
    # =============================
    skills = []
    for category in resume.skill_categories.all():
        for skill in category.skills.all():
            skills.append(skill.name)

    if skills:
        p = doc.add_paragraph()
        run = p.add_run("\nSkills\n")
        run.bold = True
        run.font.size = Pt(14)

        table = doc.add_table(rows=1, cols=3)
        cols = table.rows[0].cells

        col1 = skills[0::3]
        col2 = skills[1::3]
        col3 = skills[2::3]

        for i, col_data in enumerate([col1, col2, col3]):
            for skill in col_data:
                cols[i].add_paragraph(f"• {skill}")

    # =============================
    # EXPERIENCE
    # =============================
    if resume.journey.all():
        p = doc.add_paragraph()
        run = p.add_run("\nWork Experience\n")
        run.bold = True
        run.font.size = Pt(14)

        for journey in resume.journey.all():
            for item in journey.excellences.all():
                p = doc.add_paragraph()
                run = p.add_run(item.title + "\n")
                run.bold = True

                p.add_run(f"{item.company} | {item.date_range}\n")
                p.add_run(item.description)

    # =============================
    # CERTIFICATIONS (2 COLUMN)
    # =============================
    certs = []
    for profession in resume.professions.all():
        for cert in profession.certifications.all():
            if cert.is_active:
                certs.append(cert.title)

    if certs:
        p = doc.add_paragraph()
        run = p.add_run("\nCertifications\n")
        run.bold = True
        run.font.size = Pt(14)

        table = doc.add_table(rows=1, cols=2)
        cols = table.rows[0].cells

        col1 = certs[0::2]
        col2 = certs[1::2]

        for i, col_data in enumerate([col1, col2]):
            for cert in col_data:
                cols[i].add_paragraph(f"• {cert}")

    # =============================
    # EDUCATION
    # =============================
    if resume.journeys.all():
        p = doc.add_paragraph()
        run = p.add_run("\nEducation\n")
        run.bold = True
        run.font.size = Pt(14)

        for item in resume.journeys.all():
            if item.is_active:
                doc.add_paragraph(f"{item.description} ({item.year})")

    # =============================
    # SAVE FILE
    # =============================
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
