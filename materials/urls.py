from django.urls import path

from .views import MaterialListView, AddMaterialView, UpdateMaterialView, AdditiveListView, AddAdditiveView, \
    UpdateAdditiveView

app_name = 'materials'

urlpatterns = [
    path('', MaterialListView.as_view(), name='list_materials'),
    path('add/', AddMaterialView.as_view(), name='add_material'),
    path('<int:pk>/', UpdateMaterialView.as_view(), name='update_material'),
    path('additive/',AdditiveListView.as_view(), name='list_additives'),
    path('additive/add/', AddAdditiveView.as_view(), name='add_additive'),
    path('additive/<int:pk>/', UpdateAdditiveView.as_view(), name='update_additive'),



]
