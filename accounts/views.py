from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
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
        menu_items.append({'title': 'Add to scrap log', 'url': reverse('jobs:add_scrap_log'),'icon': 'recycle', 'color': 'text-success'})

    if user.is_authenticated:

        user_groups = list(user.groups.values_list('name', flat=True))

        # АКО Е SUPERUSER
        if user.is_superuser:
            menu_items.extend([
                {'title': 'QC Logging', 'url': reverse('qcloging:list_qc_logs'), 'icon': 'journal-check', 'color': 'text-primary'},
                {'title': 'Jobs', 'url': reverse('jobs:list_jobs'), 'icon': 'briefcase', 'color': 'text-primary'},
                {'title': 'Trading Parties', 'url': reverse('traidingparties:add_supplier'), 'icon': 'building', 'color': 'text-primary'},
                {'title': 'Accounts (HR)', 'url': 'http://localhost:5173', 'icon': 'person-gear', 'color': 'text-info'},
                {'title': 'Materials', 'url': reverse('materials:list_materials'), 'icon': 'box-seam', 'color': 'text-warning'},
                {'title': 'Tools', 'url': reverse('equipment:tool-list'), 'icon': 'tools', 'color': 'text-warning'},
                {'title': 'Machine', 'url': reverse('equipment:machine-list'), 'icon': 'machines', 'color': 'text-warning'},
                {'title': 'Създай QC Issue', 'url': reverse('qcloging:add_qc_issue'), 'icon': 'exclamation-octagon', 'color': 'text-danger'},
                {'title': 'Job Log', 'url': reverse('jobs:list_jobs_logs'), 'icon': 'clipboard-data', 'color': 'text-secondary'},
                {'title': 'Scrap Reason', 'url': reverse('jobs:add_scrap_reason'), 'icon': 'clipboard-data','color': 'text-secondary'},
            ])

            return render(request, 'shared/template.html', {'menu_items': menu_items})

        # 2. QC МЕНИДЖЪР
        if 'QC Manager' in user_groups:
            menu_items.extend([
                {'title': 'QC Logging', 'url': reverse('qcloging:list_qc_logs'), 'icon': 'journal-check', 'color': 'text-primary'},
                {'title': 'Jobs', 'url': reverse('jobs:list_jobs'), 'icon': 'briefcase', 'color': 'text-primary'},
                {'title': 'Trading Parties', 'url': reverse('traidingparties:add_supplier'), 'icon': 'building', 'color': 'text-primary'},
                {'title': 'Scrap Reason', 'url': reverse('jobs:add_scrap_reason'), 'icon': 'clipboard-data','color': 'text-secondary'},
                {'title': 'Materials', 'url': reverse('materials:list_materials'), 'icon': 'box-seam','color': 'text-warning'},
            ])




        # 3. HR (Accounts CRUD)
        if 'HR' in user_groups:
            menu_items.append({'title': 'Accounts (HR)', 'url': 'http://localhost:5173', 'icon': 'person-gear', 'color': 'text-info'})

        # 4. PRODUCTION MANAGER (Materials & Equipment)
        if any(group.lower() == 'production manager' for group in user_groups):
            menu_items.extend([
                {'title': 'Materials', 'url': reverse('materials:list_materials'), 'icon': 'box-seam', 'color': 'text-warning'},
                {'title': 'Tools', 'url': reverse('equipment:tool-list'), 'icon': 'tools', 'color': 'text-warning'},
                {'title': 'Machine', 'url': reverse('equipment:machine-list'), 'icon': 'machines','color': 'text-warning'},
                {'title': 'Trading Parties', 'url': reverse('traidingparties:add_supplier'), 'icon': 'building','color': 'text-primary'},
            ])

        # 5. SUPERVISOR, QC INSPECTOR, TEAM LEADER (QC Issue Creation)
        special_roles = ['Supervisor', 'Supervisors', 'QC Inspector', 'Team Leader']
        if any(role in user_groups for role in special_roles):
            menu_items.extend([
                {'title': 'Създай QC Issue', 'url': reverse('qcloging:add_qc_issue'), 'icon': 'exclamation-octagon', 'color': 'text-danger'},
                {'title': 'Job Log', 'url': reverse('jobs:list_jobs_logs'), 'icon': 'clipboard-data', 'color': 'text-secondary'},
                {'title': 'QC Logging', 'url': reverse('qcloging:list_qc_logs'), 'icon': 'journal-check','color': 'text-primary'},
            ])
        # 6. COLOURMEN (JobLog & Скрап)
        if 'Colourmen' in user_groups:
            menu_items.append({'title': 'Job Log', 'url': reverse('jobs:list_jobs_logs'), 'icon': 'clipboard-data', 'color': 'text-secondary'})

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
