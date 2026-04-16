from django.contrib import admin
from reports.models import ReportConfiguration, ReportParameter
# Register your models here.




# Register your models here.

@admin.register(ReportConfiguration)
class ReportConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'method_name')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')



@admin.register(ReportParameter)
class ReportParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'report',)
    search_fields = ('name', 'label')
    list_filter = ('name', 'label')
