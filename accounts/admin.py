from django.contrib import admin

from accounts.models import *


# Register your models here.
@admin.register(WorkPosition)
class WorkPositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('username', 'email')
    

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'clock_number', 'work_position')
    list_filter = ('work_position',)
    search_fields = ('first_name', 'last_name', 'clock_number')
    
    

    