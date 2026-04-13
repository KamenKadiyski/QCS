from django.contrib import admin

from traidingparties.models import *


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer_own_labeling')
    search_fields = ('name',)
    list_filter = ('customer_own_labeling',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'mail')
    search_fields = ('name',)

@admin.register(DeliveryQualityIssue)
class DeliveryQualityIssueAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'material', 'additive', 'issue_date')
    list_filter = ('supplier',)
    search_fields = ('supplier__name', 'material__name', 'additive__name')