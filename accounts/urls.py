from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import home_view, WorkPositionViewSet, EmployeeViewSet, LogoutView, ChangePasswordView, accounts_management_view
app_name = 'accounts'

router = DefaultRouter()
router.register(r'positions', WorkPositionViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('manage/', accounts_management_view, name='manage_accounts'),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/logout/', LogoutView.as_view(), name='token_logout'),
    path('api/password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True), name='login'),
    path(
        'password/change/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change_form.html',
            success_url=reverse_lazy('accounts:password_change_done'),
        ),
        name='password_change',
    ),
    path(
        'password/change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
        name='password_change_done',
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:home'), name='logout'),
]
