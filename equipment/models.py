from django.db import models

from equipment.validators import min_value_validator


# Create your models here.
#Модел за описване на сградите според технически показатели
class Building(models.Model):
    name = models.CharField(max_length=100)
    crane_capacity=models.IntegerField(validators=[min_value_validator])
    number_of_silos=models.PositiveIntegerField()
    is_centralised_cooling=models.BooleanField()

    def __str__(self):
        return self.name
#Модел за описание на матриците. Описват се основните параметри, за да се прецени дали са съвместими с дадена машина
class Tool(models.Model):
    code=models.CharField(max_length=10)
    description=models.TextField()
    clamping_force=models.IntegerField(validators=[min_value_validator])
    tool_width=models.FloatField(validators=[min_value_validator])
    tool_height=models.FloatField(validators=[min_value_validator])
    tool_thickness=models.FloatField(validators=[min_value_validator])
    moving_platen_stroke=models.FloatField(validators=[min_value_validator])
    injection_capacity=models.FloatField(validators=[min_value_validator])
    ejecting_stroke=models.FloatField(validators=[min_value_validator])
    number_of_ejector_cores=models.IntegerField(validators=[min_value_validator])
    is_in_use = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.code} - {self.description}'

#Модел за описание на машината. Задават се максималните критерии, според които се определят
#съвместимите матрици с машината.
class Machine(models.Model):
    machine_number=models.CharField(max_length=10)
    building=models.ForeignKey(Building, on_delete=models.CASCADE)
    machine_model=models.CharField(max_length=20)
    machine_description=models.TextField()
    max_clamping_force=models.IntegerField(validators=[min_value_validator])
    max_tool_width=models.FloatField(validators=[min_value_validator])
    max_tool_height=models.FloatField(validators=[min_value_validator])
    max_tool_thickness=models.FloatField(validators=[min_value_validator])
    max_moving_platen_stroke=models.FloatField(validators=[min_value_validator])
    max_injection_capacity=models.FloatField(validators=[min_value_validator])
    max_ejecting_stroke=models.FloatField(validators=[min_value_validator])
    number_of_ejector_cores=models.IntegerField(validators=[min_value_validator])
    compatible_tools=models.ManyToManyField(Tool, related_name='compatible_machines')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['machine_number', 'building'], name='machine_code')
        ]

    def __str__(self):
        return f'{self.machine_number} - {self.machine_model}'

#Модел на формуляр за искане за ремонт на матрица
class ToolRepairRequest(models.Model):
    tool=models.ForeignKey(Tool,related_name='repairs' ,on_delete=models.CASCADE)
    reason_for_repair=models.TextField()
    request_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    request_status=models.CharField(
        max_length=30,
        choices=(
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('repair in progress', 'Repair in progress'),
            ('repair completed', 'Repair completed')
        ),
    )
    additional_notes=models.TextField(blank=True, null=True)
    def __str__(self):
        return f'{self.tool.code} - {self.request_status}'


