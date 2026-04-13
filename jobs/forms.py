from django import forms

from jobs.models import *


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'materials': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'additives': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'tools': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'qc_and_additional_notes': forms.Textarea(attrs={'class': 'form-control'}),
        }

class AddToJobLogForm(forms.ModelForm):
    class Meta:
        model = JobLog
        exclude = 'date_and_time',




