from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from equipment.models import Tool, Machine
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
        fields = ['job', 'order_total_amount', 'current_material',
                  'current_additive', 'current_tool', 'current_machine', 'is_complete']
        # Widgets са преместени тук за автоматично стилизиране
        widgets = {
            'job': forms.Select(attrs={'class': 'form-select'}),
            'order_total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_material': forms.Select(attrs={'class': 'form-select'}),
            'current_additive': forms.Select(attrs={'class': 'form-select'}),
            'current_tool': forms.Select(attrs={'class': 'form-select'}),
            'current_machine': forms.Select(attrs={'class': 'form-select'}),
            'is_complete': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Вземаме избраните ID-та от POST данните или от инстанцията
        job_id = self.data.get('job') or (self.instance.job.id if self.instance.pk else None)
        tool_id = self.data.get('current_tool') or (self.instance.current_tool.id if self.instance.pk else None)

        # 2. Филтриране на МАТРИЦИТЕ спрямо избраната Работа
        if job_id:
            try:
                selected_job = Job.objects.get(id=job_id)
                tool_qs = selected_job.tools.filter(is_in_use=False)
                if self.instance.pk:
                    tool_qs |= Tool.objects.filter(pk=self.instance.current_tool.pk)
                self.fields['current_tool'].queryset = tool_qs
            except (Job.DoesNotExist, ValueError):
                self.fields['current_tool'].queryset = Tool.objects.none()
        else:
            self.fields['current_tool'].queryset = Tool.objects.none()

        # 3. Филтриране на МАШИНИТЕ спрямо избраната Матрица
        if tool_id:
            try:
                selected_tool = Tool.objects.get(id=tool_id)
                # Филтрираме машините, които са съвместими с ТАЗИ матрица и са свободни
                machine_qs = Machine.objects.filter(
                    compatible_tools=selected_tool,
                    is_in_use=False
                )
                if self.instance.pk:
                    machine_qs |= Machine.objects.filter(pk=self.instance.current_machine.pk)
                self.fields['current_machine'].queryset = machine_qs
            except (Tool.DoesNotExist, ValueError):
                self.fields['current_machine'].queryset = Machine.objects.none()
        else:
            # Ако още няма избрана матрица, показваме всички свободни машини
            # или можем да ги оставим празни, докато не се избере матрица
            self.fields['current_machine'].queryset = Machine.objects.filter(is_in_use=False)

    def clean_current_tool(self):
        tool = self.cleaned_data.get('current_tool')
        if not self.instance.pk and tool and tool.is_in_use:
            raise ValidationError(f"Матрица {tool.code} вече се използва!")
        return tool

    def clean_current_machine(self):
        machine = self.cleaned_data.get('current_machine')
        if not self.instance.pk and machine and machine.is_in_use:
            raise ValidationError(f"Машина {machine.machine_number} вече се използва!")
        return machine

    def clean(self):
        cleaned_data = super().clean()
        tool = cleaned_data.get('current_tool')
        machine = cleaned_data.get('current_machine')
        job = cleaned_data.get('job')

        if tool and machine:
            if not machine.compatible_tools.filter(id=tool.id).exists():
                raise ValidationError(f"Матрица {tool.code} не е съвместима с машина {machine.machine_number}!")

        if job and tool:
            if tool not in job.tools.all():
                raise ValidationError(f"Матрица {tool.code} не е част от поръчка {job.job_code}!")
        return cleaned_data
