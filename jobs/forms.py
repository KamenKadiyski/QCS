from django import forms
from django.core.exceptions import ValidationError
from materials.models import Material, Additive
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
        fields = [
            'job', 'order_total_amount', 'current_material',
            'current_additive', 'current_tool', 'current_machine', 'is_complete'
        ]
        widgets = {
            'job': forms.Select(attrs={'class': 'form-select', 'onchange': 'this.form.submit()'}),
            'order_total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_material': forms.Select(attrs={'class': 'form-select'}),
            'current_additive': forms.Select(attrs={'class': 'form-select'}),
            'current_tool': forms.Select(attrs={'class': 'form-select', 'onchange': 'this.form.submit()'}),
            'current_machine': forms.Select(attrs={'class': 'form-select'}),
            'is_complete': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        job_id = self.data.get('job') or (self.instance.job.id if self.instance.pk else None)
        tool_id = self.data.get('current_tool') or (self.instance.current_tool.id if self.instance.pk else None)

        if job_id:
            try:
                selected_job = Job.objects.get(id=job_id)
                self.fields['current_material'].queryset = selected_job.materials.all()
                self.fields['current_additive'].queryset = selected_job.additives.all()
                tool_qs = selected_job.tools.filter(is_in_use=False)
                if self.instance.pk and self.instance.current_tool:
                    tool_qs |= Tool.objects.filter(pk=self.instance.current_tool.pk)
                self.fields['current_tool'].queryset = tool_qs

            except (Job.DoesNotExist, ValueError):
                self._set_empty_dependent_fields()
        else:
            self._set_empty_dependent_fields()

        if tool_id:
            try:
                selected_tool = Tool.objects.get(id=tool_id)
                machine_qs = Machine.objects.filter(compatible_tools=selected_tool, is_in_use=False)
                if self.instance.pk and self.instance.current_machine:
                    machine_qs |= Machine.objects.filter(pk=self.instance.current_machine.pk)
                self.fields['current_machine'].queryset = machine_qs
            except (Tool.DoesNotExist, ValueError):
                self.fields['current_machine'].queryset = Machine.objects.none()
        else:
            self.fields['current_machine'].queryset = Machine.objects.filter(is_in_use=False)

    def _set_empty_dependent_fields(self):
        self.fields['current_material'].queryset = Material.objects.none()
        self.fields['current_additive'].queryset = Additive.objects.none()
        self.fields['current_tool'].queryset = Tool.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        job = cleaned_data.get('job')
        material = cleaned_data.get('current_material')
        additive = cleaned_data.get('current_additive')
        tool = cleaned_data.get('current_tool')
        machine = cleaned_data.get('current_machine')

        if job:
            if material and material not in job.materials.all():
                self.add_error('current_material', f"The material is not associated with a job. {job.job_code}!")
            if additive and additive not in job.additives.all():
                self.add_error('current_additive', f"The additive is not part of the job specification {job.job_code}!")
            if tool and tool not in job.tools.all():
                self.add_error('current_tool', f"The tool is not part of a job {job.job_code}!")
        if tool and machine and not machine.compatible_tools.filter(id=tool.id).exists():
            raise ValidationError(f"Tool {tool.code} is not compatible with machine {machine.machine_number}!")

        return cleaned_data

    def clean_current_tool(self):
        tool = self.cleaned_data.get('current_tool')
        if not self.instance.pk and tool and tool.is_in_use:
            raise ValidationError(f"The tool {tool.code} is already in use!")
        return tool

    def clean_current_machine(self):
        machine = self.cleaned_data.get('current_machine')
        if not self.instance.pk and machine and machine.is_in_use:
            raise ValidationError(f"Machine {machine.machine_number} is already in use!")
        return machine
