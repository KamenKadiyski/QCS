from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from .models import Employee, WorkPosition

User = get_user_model()
# Create your tests here.
class EmployeeSignalTest(TestCase):
    def setUp(self):
        self.pos_qc = WorkPosition.objects.create(name="QC Inspector")
        self.pos_admin = WorkPosition.objects.create(name="Administrator")
        self.pos_other = WorkPosition.objects.create(name="Cleaner")
        self.pos_supervisor = WorkPosition.objects.create(name="Supervisor")
        self.pos_team_leader = WorkPosition.objects.create(name="Team Leader")
        Group.objects.create(name="QC Inspector")
        Group.objects.create(name="QC Manager")
        Group.objects.create(name="Supervisors")

    def test_user_creation_with_correct_role_and_slug(self):
        emp = Employee.objects.create(
            first_name="Andy",
            last_name="Holt",
            clock_number="1001",
            work_position=self.pos_qc,
            login_required=True
        )
        emp.refresh_from_db()

        self.assertIsNotNone(emp.user)
        self.assertEqual(emp.user.username, "andy-holt")
        self.assertEqual(emp.user.role, "qc")
        self.assertFalse(emp.user.is_staff)
        # Проверка на имейла в опашката
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("andy-holt", mail.outbox[0].body)

    def test_is_staff_assignment_for_admin_role(self):
        emp = Employee.objects.create(
            first_name="Admin",
            last_name="User",
            clock_number="9999",
            work_position=self.pos_admin,
            login_required=True
        )
        emp.refresh_from_db()
        self.assertTrue(emp.user.is_staff)
        self.assertEqual(emp.user.role, "admin")

    def test_username_collision_handling(self):
        Employee.objects.create(
            first_name="Gary", last_name="Ireland",
            clock_number="G1", work_position=self.pos_other, login_required=True
        )
        # Втори потребител със същото име
        emp2 = Employee.objects.create(
            first_name="Gary", last_name="Ireland",
            clock_number="G2", work_position=self.pos_other, login_required=True
        )
        emp2.refresh_from_db()

        self.assertEqual(emp2.user.username, "gary-ireland2")

    def test_no_login_no_user(self):
        emp = Employee.objects.create(
            first_name="No",
            last_name="Login",
            clock_number="0000",
            work_position=self.pos_other,
            login_required=False
        )
        self.assertIsNone(emp.user)
        self.assertEqual(len(mail.outbox), 0)

    def test_default_role_mapping(self):
        emp = Employee.objects.create(
            first_name="Blagovest",
            last_name="Position",
            clock_number="5555",
            work_position=self.pos_other,
            login_required=True
        )
        emp.refresh_from_db()
        self.assertEqual(emp.user.role, "operator")

    def test_user_gets_expected_qc_group(self):
        emp = Employee.objects.create(
            first_name="Lee",
            last_name="Inspector",
            clock_number="2001",
            work_position=self.pos_qc,
            login_required=True,
        )
        emp.refresh_from_db()
        self.assertEqual(emp.user.groups.count(), 1)
        self.assertEqual(emp.user.groups.first().name, "QC Inspector")

    def test_supervisor_role_maps_to_supervisors_group_alias(self):
        emp = Employee.objects.create(
            first_name="Ste",
            last_name="Supervisor",
            clock_number="2002",
            work_position=self.pos_supervisor,
            login_required=True,
        )
        emp.refresh_from_db()
        self.assertEqual(emp.user.role, "supervisor")
        self.assertEqual(emp.user.groups.count(), 1)
        self.assertEqual(emp.user.groups.first().name, "Supervisors")

    def test_missing_group_is_created_and_assigned(self):
        Group.objects.filter(name="Team Leader").delete()
        emp = Employee.objects.create(
            first_name="Kamen",
            last_name="Leader",
            clock_number="2003",
            work_position=self.pos_team_leader,
            login_required=True,
        )
        emp.refresh_from_db()
        self.assertEqual(emp.user.groups.count(), 1)
        self.assertEqual(emp.user.groups.first().name, "Team Leader")
        self.assertTrue(Group.objects.filter(name="Team Leader").exists())


class ChangePasswordAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="pass-user",
            password="OldPass123!",
            role="operator",
        )
        self.url = reverse("accounts:change_password")

    def test_authenticated_user_can_change_own_password(self):
        self.client.login(username="pass-user", password="OldPass123!")
        response = self.client.post(
            self.url,
            data={"old_password": "OldPass123!", "new_password": "NewPass456!"},
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPass456!"))

    def test_change_password_rejects_wrong_old_password(self):
        self.client.login(username="pass-user", password="OldPass123!")
        response = self.client.post(
            self.url,
            data={"old_password": "WrongOldPass!", "new_password": "NewPass456!"},
        )

        self.assertEqual(response.status_code, 400)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("OldPass123!"))

    def test_change_password_requires_authentication(self):
        response = self.client.post(
            self.url,
            data={"old_password": "OldPass123!", "new_password": "NewPass456!"},
        )
        self.assertIn(response.status_code, [401, 403])

    def test_home_page_contains_change_password_button_for_authenticated_user(self):
        self.client.login(username="pass-user", password="OldPass123!")
        response = self.client.get(reverse("accounts:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("accounts:password_change"))

    def test_password_change_form_page_is_available_for_authenticated_user(self):
        self.client.login(username="pass-user", password="OldPass123!")
        response = self.client.get(reverse("accounts:password_change"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Change Password")
