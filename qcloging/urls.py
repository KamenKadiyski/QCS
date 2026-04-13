from django.urls import path
from django.views import View

from .views import AddToQCLogView, JobLogListView, UpdateQCLogView, QCIssueListView, AddToQCIssueView, UpdateQCIssueView

app_name = 'qcloging'

urlpatterns = [
    path('', JobLogListView.as_view(), name='list_qc_logs'),
    path('add_to_qc_log/', AddToQCLogView.as_view(), name='add_qc_log'),
    path('qc/update/<int:pk>/', UpdateQCLogView.as_view(), name='update_qc_log'),
    path('qc-issue/',QCIssueListView.as_view(),name='list_qc_issues'),
    path('add_to_qc_issue/',AddToQCIssueView.as_view(),name='add_qc_issue'),
    path('qc-issue/update/<int:pk>/',UpdateQCIssueView.as_view(),name='update_qc_issue'),



]
