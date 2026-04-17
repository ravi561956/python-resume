from django.urls import path
from .views import resume_view
from .views import submit_contact_form
from .views import download_resume_pdf, download_resume_docx
from .views import preview_resume_pdf

urlpatterns = [
    path('', resume_view, name='resume'),
    path('contact/submit/', submit_contact_form, name='contact_submit'),
    path('resume/', resume_view, name='resume'),
    path('resume/pdf/', download_resume_pdf, name='resume_pdf'),
    path('resume/doc/', download_resume_docx, name='resume_doc'),
    path('preview-pdf/<int:pk>/', preview_resume_pdf, name='resume_pdf_preview'),
]
