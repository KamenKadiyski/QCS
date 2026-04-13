from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# HR - позициите на служителите
class WorkPosition(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

#Разширение на User модела. Според ролята се определят и permissions
class User(AbstractUser):
    ROLE_CHOICES = (
            ("operator", "Operator"),
            ("qc", "Quality Control"),
            ("manager", "Manager"),
            ("admin", "Administrator"),
            ("qc manager", "QC Manager"),
            ("supervisor", "Supervisor"),
            ("team leader", "Team Leader"),
            ("colourman", "Colourman"),
            ("production manager", "Production Manager")
        )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
# HR - служителите на фирмата. Когато се изтрие user, HR записа остава за да се пази
#история от логовете.
class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    clock_number = models.CharField(max_length=20,unique=True)
    work_position = models.ForeignKey(WorkPosition, on_delete=models.CASCADE)
    login_required = models.BooleanField(default=False)
    user = models.OneToOneField(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name='employee_profile')
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


