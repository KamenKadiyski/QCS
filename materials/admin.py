from django.contrib import admin

from materials.models import *


# Register your models here.
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'type')
    list_filter = ('supplier', 'type')
    search_fields = ('name',)


@admin.register(Additive)
class AdditiveAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier')
    list_filter = ('supplier',)
    search_fields = ('name',)

