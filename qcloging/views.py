from django.views.generic import CreateView, ListView, UpdateView
from django import forms
from rest_framework.reverse import reverse_lazy

from jobs.models import JobLog
from .models import QCLog, QCIssue


# Create your views here.
class JobLogListView(ListView):
    model = QCLog
    template_name = 'qcloging/list_qc_logs.html'
    page_title = 'QC Logs list'

    def get_queryset(self):
        queryset = QCLog.objects.select_related('job_log', 'qc_inspector').all().order_by('-logged_at')
        date_query = self.request.GET.get('date_filter')

        if date_query:

            queryset = queryset.filter(logged_at__date=date_query)
        return queryset




class AddToQCLogView(CreateView):
    model = QCLog
    fields = [
        'job_log', 'first_of_sample_issued', 'like_fos', 'have_spec_sheet',
        'correct_labels', 'packed_correctly', 'operator_sheet_signed', 'runs_with_flash'
    ]
    template_name = 'qcloging/add_to_qc_log.html'
    success_url = reverse_lazy('qcloging:list_qc_logs')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['job_log'].queryset = JobLog.objects.filter(is_complete=False)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        if hasattr(self.request.user, 'employee_profile'):
            form.instance.qc_inspector = self.request.user.employee_profile
            return super().form_valid(form)
        else:
            form.add_error(None, "Your user does not have an associated Employee account!")
            return self.form_invalid(form)





class UpdateQCLogView(UpdateView):
    model = QCLog
    fields = '__all__'
    template_name = 'qcloging/update_qc_log.html'
    success_url = reverse_lazy('qcloging:list_qc_logs')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        return form





class QCIssueListView(ListView):
    model = QCIssue
    template_name = 'qcloging/list_qc_issues.html'
    page_title = 'QC Issues list'
    def get_queryset(self):
        queryset = QCIssue.objects.select_related('job_log', 'assigned_to').all().order_by('-logged_at')
        date_query = self.request.GET.get('date_filter')
        if date_query:
            queryset = queryset.filter(logged_at__date=date_query)
        return queryset


class AddToQCIssueView(CreateView):
    model = QCIssue
    fields = ['job_log', 'issue_description', 'assigned_to', 'is_sorted']
    template_name = 'qcloging/add_to_qc_issue.html'
    success_url = reverse_lazy('qcloging:list_qc_issues')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['job_log'].queryset = JobLog.objects.filter(is_complete=False)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control shadow-sm'})
        return form

class UpdateQCIssueView(UpdateView):
    model = QCIssue
    fields = ['job_log', 'issue_description', 'assigned_to', 'is_sorted']
    template_name = 'qcloging/update_qc_issue.html'
    success_url = reverse_lazy('qcloging:list_qc_issues')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control shadow-sm'})
        return form




