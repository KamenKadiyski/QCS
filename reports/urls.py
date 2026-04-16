from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('<str:report_slug>/', views.report_view, name='report_view'),
    path('stats/', views.stats, name='daily_stats')

]