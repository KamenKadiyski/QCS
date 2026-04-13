from django.db import models

# Create your models here.
#Модела описва формуляр за проверка на определени показатели за работата.
class QCLog(models.Model):
    job_log=models.ForeignKey('jobs.JobLog', on_delete=models.CASCADE,related_name='qc_logs')
    qc_inspector=models.ForeignKey('accounts.Employee', on_delete=models.CASCADE,related_name='employee_logs')
    first_of_sample_issued=models.BooleanField(default=False)
    like_fos=models.BooleanField(default=False)
    have_spec_sheet=models.BooleanField(default=False)
    correct_labels=models.BooleanField(default=False)
    packed_correctly=models.BooleanField(default=False)
    operator_sheet_signed=models.BooleanField(default=False)
    runs_with_flash=models.BooleanField(default=False)
    logged_at=models.DateTimeField(auto_now_add=True)

#Модела описва открити проблеми с качеството.
class QCIssue(models.Model):
    job_log=models.ForeignKey('jobs.JobLog', on_delete=models.CASCADE, related_name='qc_issues')
    issue_description=models.TextField()
    assigned_to=models.ForeignKey('accounts.Employee', on_delete=models.CASCADE, related_name='setter_issues')
    is_sorted=models.BooleanField(default=False)
    logged_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)