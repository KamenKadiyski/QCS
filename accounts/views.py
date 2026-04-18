from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.urls import reverse_lazy
from django.urls.base import reverse
from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Employee, WorkPosition
from .serializers import EmployeeSerializer, WorkPositionSerializer, ChangePasswordSerializer


# Проверка дали потребителят е HR или Superuser
def is_hr_or_admin(user):
    return user.is_superuser or user.groups.filter(name='HR').exists()


@login_required(login_url=reverse_lazy('accounts:login'))
@user_passes_test(is_hr_or_admin, login_url=reverse_lazy('accounts:login'))
def accounts_management_view(request):
    return render(request, 'accounts/manage_employees.html')



class WorkPositionViewSet(viewsets.ModelViewSet):
    queryset = WorkPosition.objects.all()
    serializer_class = WorkPositionSerializer
    permission_classes = [permissions.AllowAny]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = None



def home_view(request):
    user = request.user
    menu_items = []

    # 1. ОБЩОДОСТЪПНИ
    if not user.is_authenticated or user.role!='hr':
        menu_items.append({'title': 'Add to scrap log','url': reverse('jobs:add_scrap_log'),'icon': 'bi bi-recycle','color': 'text-success'})

    if user.is_authenticated:

        user_groups = list(user.groups.values_list('name', flat=True))

        # АКО Е SUPERUSER
        if user.is_superuser:
            menu_items.extend([

                {'title': 'Scrap Reason', 'url': reverse('jobs:add_scrap_reason'), 'icon': 'bi bi-recycle','color': 'text-danger'},
                {'title': 'QC Logging', 'url': reverse('qcloging:list_qc_logs'), 'icon': 'bi bi-clipboard2-check-fill','color': 'text-primary'},
                {'title': 'Create QC Issue', 'url': reverse('qcloging:add_qc_issue'),'icon': 'bi bi-exclamation-triangle-fill', 'color': 'text-danger'},
                {'title': 'Jobs', 'url': reverse('jobs:list_jobs'), 'icon': 'bi bi-stack', 'color': 'text-primary'},
                {'title': 'Job Log', 'url': reverse('jobs:list_jobs_logs'), 'icon': 'bi bi-stopwatch','color': 'text-secondary'},
                {'title': 'Trading Parties', 'url': reverse('traidingparties:add_supplier'), 'icon': 'bi bi-truck','color': 'text-primary'},
                {'title': 'Accounts (HR)', 'url': reverse('accounts:manage_accounts'), 'icon': 'bi bi-people-fill','color': 'text-info'},
                {'title': 'Materials', 'url': reverse('materials:list_materials'), 'icon': 'bi bi-moisture','color': 'text-warning'},
                {'title': 'Tools', 'url': reverse('equipment:tool-list'), 'icon': 'bi bi-grid-3x3-gap-fill','color': 'text-warning'},
                {'title': 'Machine', 'url': reverse('equipment:machine-list'), 'icon': 'bi bi-cpu-fill','color': 'text-warning'},
                {'title': 'Reports', 'url': reverse('reports:report_list'), 'icon': 'bi bi-graph-up-arrow','color': 'text-secondary'},
            ])

            return render(request, 'shared/template.html', {'menu_items': menu_items})

        # 2. QC МЕНИДЖЪР
        if 'QC Manager' in user_groups:
            menu_items.extend([
                {'title': 'Scrap Reason', 'url': reverse('jobs:add_scrap_reason'), 'icon': 'bi bi-recycle','color': 'text-danger'},
                {'title': 'QC Logging', 'url': reverse('qcloging:list_qc_logs'), 'icon': 'bi bi-clipboard2-check-fill','color': 'text-primary'},
                {'title': 'Jobs', 'url': reverse('jobs:list_jobs'), 'icon': 'bi bi-stack', 'color': 'text-primary'},
                {'title': 'Trading Parties', 'url': reverse('traidingparties:add_supplier'), 'icon': 'bi bi-truck','color': 'text-primary'},
                {'title': 'Materials', 'url': reverse('materials:list_materials'), 'icon': 'bi bi-moisture','color': 'text-warning'},
                {'title': 'Reports', 'url': reverse('reports:report_list'), 'icon': 'bi bi-graph-up-arrow','color': 'text-secondary'},
            ])




        # 3. HR (Accounts CRUD)
        if 'HR' in user_groups:
            menu_items.append({'title': 'Accounts (HR)', 'url': reverse('accounts:manage_accounts'), 'icon': 'bi bi-people-fill','color': 'text-info'})

        # 4. PRODUCTION MANAGER (Materials & Equipment)
        if any(group.lower() == 'production manager' for group in user_groups):
            menu_items.extend([
                {'title': 'Materials', 'url': reverse('materials:list_materials'), 'icon': 'bi bi-moisture','color': 'text-warning'},
                {'title': 'Tools', 'url': reverse('equipment:tool-list'), 'icon': 'bi bi-grid-3x3-gap-fill','color': 'text-warning'},
                {'title': 'Machine', 'url': reverse('equipment:machine-list'), 'icon': 'bi bi-cpu-fill','color': 'text-warning'},
                {'title': 'Trading Parties', 'url': reverse('traidingparties:add_supplier'), 'icon': 'bi bi-truck','color': 'text-primary'},
                {'title': 'Reports', 'url': reverse('reports:report_list'), 'icon': 'bi bi-graph-up-arrow','color': 'text-secondary'},
            ])

        # 5. SUPERVISOR, QC INSPECTOR, TEAM LEADER (QC Issue Creation)
        special_roles = ['Supervisor', 'Supervisors', 'QC Inspector', 'Team Leader']
        if any(role in user_groups for role in special_roles):
            menu_items.extend([
                {'title': 'Create QC Issue', 'url': reverse('qcloging:add_qc_issue'),'icon': 'bi bi-exclamation-triangle-fill', 'color': 'text-danger'},
                {'title': 'Job Log', 'url': reverse('jobs:list_jobs_logs'), 'icon': 'bi bi-stopwatch','color': 'text-secondary'},
                {'title': 'QC Logging', 'url': reverse('qcloging:list_qc_logs'), 'icon': 'bi bi-clipboard2-check-fill','color': 'text-primary'},
            ])
        # 6. COLOURMEN (JobLog & Скрап)
        if 'Colourmen' in user_groups:
            menu_items.append({'title': 'Job Log', 'url': reverse('jobs:list_jobs_logs'), 'icon': 'bi bi-stopwatch','color': 'text-secondary'},)

    return render(request, 'shared/template.html', {'menu_items': menu_items})




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=205)
        except Exception:
            return Response(status=400)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        update_session_auth_hash(request, user)

        return Response({"detail": "Password changed successfully."}, status=200)
