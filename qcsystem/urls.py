"""
URL configuration for qcsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include

from accounts.views import home_view
from shared.views import custom_error_404, custom_error_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('equipment/', include('equipment.urls')),
    path('jobs/', include('jobs.urls')),
    path('materials/', include('materials.urls')),
    path('qcloging/', include('qcloging.urls')),
    path('reports/', include('reports.urls')),
    path('traidingparties/', include('traidingparties.urls')),


]

handler404 = custom_error_404
handler500 = custom_error_500