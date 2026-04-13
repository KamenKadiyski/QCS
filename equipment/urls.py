from django.urls import path
from rest_framework.routers import DefaultRouter

from equipment import views

app_name = 'equipment'

router = DefaultRouter()
router.register('machines', views.MachineViewSet)
router.register('tools', views.ToolViewSet)


urlpatterns = [
    path('machines/upload/', views.MachineUploadView.as_view(), name='machine-upload'),
    path('tools/upload/', views.ToolUploadView.as_view(), name='tool-upload'),
] + router.urls
