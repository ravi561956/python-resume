from docx import Document
from io import BytesIO


def generate_resume_docx(resume):
    doc = Document()

    doc.add_heading(resume.name, level=1)
    doc.add_paragraph(resume.title)

    doc.add_paragraph(f"Email: {resume.email}")
    doc.add_paragraph(f"Phone: {resume.phone}")

    doc.add_heading("Professional Summary", level=2)
    doc.add_paragraph(resume.summary)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
