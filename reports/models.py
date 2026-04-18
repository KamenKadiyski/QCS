from django.db import models

# Create your models here.


# Този модел описва Meta данните за съответният report.
# При добавянето на нов запис е важно да се въвежда правилното име на функция
# в полето method_name.

class ReportConfiguration(models.Model):
    name = models.CharField(max_length=255, verbose_name='Report name')
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    method_name = models.CharField(max_length=255,
                                   help_text='function name in reports library')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chart_label_field = models.CharField(max_length=50, blank=True, help_text="Поле за X-оста (напр. order_id)")
    chart_value_fields = models.CharField(max_length=255, blank=True, help_text="Полета за Y-оста, разделени със запетая (напр. quantity,scrap_quantity)")
    def __str__(self):
        return self.name

# Този модел дефинира параметрите на самите доклади, които после участват във филтрирането
# на данните. name задължително трябва да съответства на името на параметъра, който се подава функцията.
class ReportParameter(models.Model):
    PARAMETER_TYPES = (
        ('date', 'Date'),
        ('int', 'Integer'),
        ('str', 'String'),
        ('choice', 'Choice'),
        ('bool', 'Boolean'),
        ('static_choice', 'Static Choice'),
    )
    report = models.ForeignKey(ReportConfiguration, on_delete=models.CASCADE,related_name='parameters')
    name = models.CharField(max_length=255, help_text='Parameter name into function')
    label = models.CharField(max_length=255, help_text='Parameter label for the user')
    parameter_type = models.CharField(max_length=20, choices=PARAMETER_TYPES,
                                      help_text='Parameter type')
    source_model = models.CharField(max_length=50,
                                    blank=True, null=True,
                                    help_text='app_label.ModelName for choice parameters(optional) ')
    is_required = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} for {self.report.name}"
