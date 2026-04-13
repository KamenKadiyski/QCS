from django.contrib import admin

from jobs.models import *


# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_code', 'description', 'customer')
    list_filter = ('customer',)
    search_fields = ('job_code', 'description')

@admin.register(JobLog)
class JobLogAdmin(admin.ModelAdmin):
    list_display = ('job', 'order_total_amount','job__description')
    list_filter = ('job',)
    search_fields = ('job__job_code',)

@admin.register(ScrapReason)
class ScrapReasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(ScrapLog)
class ScrapLogAdmin(admin.ModelAdmin):
    list_display = ('job_log', 'scrap_reason', 'amount_scrap')
    list_filter = ('scrap_reason',)
    search_fields = ('job_log__job__job_code',)
