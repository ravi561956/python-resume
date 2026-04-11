from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO


def generate_resume_pdf(resume):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(f"<b>{resume.name}</b>", styles['Title']))
    content.append(Paragraph(resume.title, styles['Heading2']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(
        f"<b>Email:</b> {resume.email}<br/>"
        f"<b>Phone:</b> {resume.phone}",
        styles['Normal']
    ))

    content.append(Spacer(1, 16))
    content.append(Paragraph("<b>Professional Summary</b>", styles['Heading3']))
    content.append(Paragraph(resume.summary, styles['Normal']))

    doc.build(content)
    buffer.seek(0)
    return buffer
