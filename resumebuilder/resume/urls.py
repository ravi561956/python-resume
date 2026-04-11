from django.urls import path
from .views import resume_view
from .views import submit_contact_form
from .views import download_resume_pdf, download_resume_docx

urlpatterns = [
    path('', resume_view, name='resume'),
    path('contact/submit/', submit_contact_form, name='contact_submit'),
    path('resume/pdf/', download_resume_pdf, name='resume_pdf'),
    path('resume/doc/', download_resume_docx, name='resume_doc'),
]
