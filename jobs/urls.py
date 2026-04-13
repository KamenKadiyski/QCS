

from django.urls import path, include

from jobs.views import *

app_name = 'jobs'



urlpatterns = [
    path('create/', CreateJobView.as_view(), name='create_job'),
    path('list/', JobListView.as_view(), name='list_jobs'),
    path('<int:pk>/', JobDetailsView.as_view(), name='job_details'),
    path('update/<int:pk>/', UpdateJobView.as_view(), name='update_job'),
    path('delete/<int:pk>/', DeleteJobView.as_view(), name='delete_job'),
    path('scrap/', include([
    path('add-reason/', ScrapReasonAddView.as_view(), name='add_scrap_reason'),
        path('add-log/', ScrapLogAddView.as_view(), name='add_scrap_log'),
    ])),
    path('joblog/', include([
    path('create/', JobLogCreateView.as_view(), name='create_job_log'),
    path('list/', JobLogListView.as_view(), name='list_jobs_logs'),

])),


]
