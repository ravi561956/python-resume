from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from .models import Resume
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from .models import ContactSection
from django.http import FileResponse
from .utils.resume_pdf import generate_resume_pdf
from .utils.resume_docx import generate_resume_docx
from django.http import HttpResponse

def resume_view(request):
    resume = Resume.objects.filter(is_active=True).first()
    if not resume:
        return render(request, 'themes/no_resume.html')

    # Load template from selected theme folder
    template_name = f"themes/{resume.theme}/index.html"
    fallback = "themes/default/index.html"

    try:
        return render(request, template_name, {'resume': resume})
    except TemplateDoesNotExist:
        return render(request, fallback, {'resume': resume})


def submit_contact_form(request):
    if request.method == 'POST':
        section = ContactSection.objects.filter(is_active=True).first()
        form = ContactForm(request.POST)

        if form.is_valid() and section:
            contact = form.save(commit=False)
            contact.section = section
            contact.save()

            send_mail(
                subject=f"Contact Form: {contact.subject}",
                message=f""",
                Name: {contact.name}
                Email: {contact.email}

                Message:
                {contact.message}
                """,
                from_email=None,
                recipient_list=[section.receive_email_at],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully.")
            return redirect('#contact')

    return redirect('/')


def download_resume_pdf(request):
    resume = Resume.objects.filter(is_active=True).first()
    buffer = generate_resume_pdf(resume, request)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename="resume.pdf"
    )


def download_resume_docx(request):
    resume = Resume.objects.filter(is_active=True).first()
    buffer = generate_resume_docx(resume)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename="resume.docx"
    )

def preview_resume_pdf(request, pk):
    resume = Resume.objects.get(id=pk)
    buffer = generate_resume_pdf(resume, request)

    return HttpResponse(buffer.getvalue(), content_type='application/pdf')