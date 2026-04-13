from django.contrib import admin

from qcloging.models import *


# Register your models here.
@admin.register(QCLog)
class QCLogAdmin(admin.ModelAdmin):
    list_display = ('job_log', 'qc_inspector')
    list_filter = ('qc_inspector',)
    search_fields = ('job_log__job__job_code',)

@admin.register(QCIssue)
class QCIssueAdmin(admin.ModelAdmin):
    list_display = ('job_log', 'assigned_to')
    list_filter = ('assigned_to',)
    search_fields = ('job_log__job__job_code',)