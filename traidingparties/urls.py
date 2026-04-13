from django.urls import path
from django.views import View

from .views import SupplierCreatView, SupplierUpdateView, DeliveryQualityIssueCreateView

app_name = 'traidingparties'

urlpatterns = [
    path('', SupplierCreatView.as_view(), name='add_supplier'),
    path('<int:pk>/', SupplierUpdateView.as_view(), name='update_supplier'),
    path('issue/', DeliveryQualityIssueCreateView.as_view(), name='add_delivery_issue'),



]