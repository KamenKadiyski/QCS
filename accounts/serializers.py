from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from accounts.models import User, Employee,WorkPosition


class WorkPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPosition
        fields = ('id', 'name')



class EmployeeSerializer(serializers.ModelSerializer):
    work_position_name = ReadOnlyField(source='work_position.name')
    username = serializers.ReadOnlyField(source='user.username')
    role = serializers.ReadOnlyField(source='user.role')

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name',
                  'clock_number', 'work_position', 'work_position_name',
                  'login_required', 'username', 'role',]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_new_password(self, value):
        user = self.context["request"].user
        validate_password(value, user=user)
        return value
