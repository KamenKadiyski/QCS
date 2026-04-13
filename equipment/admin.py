from django.contrib import admin

from equipment.models import *


# Register your models here.
@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'crane_capacity', 'number_of_silos', 'is_centralised_cooling')
    list_filter = ('is_centralised_cooling',)
    search_fields = ('name',)

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('code', 'description',)
    list_filter = ('is_in_use',)
    search_fields = ('code', 'description',)

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('machine_number', 'machine_model', 'building')
    list_filter = ('building',)
    search_fields = ('machine_number', 'machine_model')

@admin.register(ToolRepairRequest)
class ToolRepairRequestAdmin(admin.ModelAdmin):
    list_display = ('tool', 'request_date', 'request_status')
    list_filter = ('request_status',)
    search_fields = ('tool__code',)
