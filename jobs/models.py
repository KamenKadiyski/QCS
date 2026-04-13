from django.db import models

# Create your models here.
# Описва се работа от гледна оборудването и материалите необходими за тази работа.
class Job(models.Model):
    job_code = models.CharField(max_length=100)
    description = models.TextField()
    customer = models.ForeignKey('traidingparties.Customer', on_delete=models.CASCADE, related_name='jobs')
    materials = models.ManyToManyField('materials.Material', related_name='jobs')
    additives = models.ManyToManyField('materials.Additive', related_name='jobs')
    tools = models.ManyToManyField('equipment.Tool', related_name='jobs')
    qc_and_additional_notes=models.TextField(blank=True,null=True)
    def __str__(self):
        return f'{self.job_code} - {self.description}'
#Модел за логване на текущите работи
class JobLog(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='logs')
    order_total_amount = models.PositiveIntegerField()
    current_material=models.ForeignKey('materials.Material', on_delete=models.CASCADE, related_name='job_material')
    current_additive=models.ForeignKey('materials.Additive', on_delete=models.CASCADE, related_name='job_additive')
    current_tool=models.ForeignKey('equipment.Tool', on_delete=models.CASCADE, related_name='job_tool')
    current_machine=models.ForeignKey('equipment.Machine', on_delete=models.CASCADE, related_name='job_machine')
    date_and_time=models.DateTimeField(auto_now_add=True)
    is_complete=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.job.job_code} - {self.job.description}'

#Модела описва причините за бракуване на част от продукцията
class ScrapReason(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    def __str__(self):
        return self.name
#Модела описва лог на бракуваната продукция.
class ScrapLog(models.Model):
    job_log=models.ForeignKey(JobLog, on_delete=models.CASCADE,related_name='scraps')
    scrap_reason=models.ForeignKey(ScrapReason, on_delete=models.CASCADE,related_name='scraps')
    amount_scrap=models.PositiveIntegerField()
    date_and_time=models.DateTimeField(auto_now_add=True)