from django import forms
from .models import Resume
from .models import Profession, ResumeStat
from .models import ContactMessage

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = '__all__'

class ProfessionForm(forms.ModelForm):
    class Meta:
        model = Profession
        fields = '__all__'
        widgets = {
            'resume_stats': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['resume_stats'].queryset = ResumeStat.objects.filter(
                resume=self.instance.resume
            )

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'subject', 'message')