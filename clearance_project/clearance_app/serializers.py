from rest_framework import serializers
from .models import *
class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name']

class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()

    class Meta:
        model = Department
        fields = ['id', 'name', 'faculty']

class ClearanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceStatus
        fields = ['id', 'status']

class StudentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    clearance_status = ClearanceStatusSerializer()

    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'full_name', 'matric_number', 'sex', 'date_of_birth', 'address', 'phone_number', 'department', 'clearance_status', 'is_cleared']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        department_data = validated_data.pop('department')
        clearance_status_data = validated_data.pop('clearance_status')
        
        department = Department.objects.get_or_create(name=department_data['name'], faculty=department_data['faculty'])[0]
        clearance_status = ClearanceStatus.objects.get_or_create(status=clearance_status_data['status'])[0]

        student = Student.objects.create(department=department, clearance_status=clearance_status, **validated_data)
        return student

class DepartmentClearanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    department = DepartmentSerializer()
    clearance_status = ClearanceStatusSerializer()

    class Meta:
        model = DepartmentClearance
        fields = ['id', 'student', 'department', 'clearance_status', 'request_date', 'update_date']

class NotificationSerializer(serializers.ModelSerializer):
    recipient = StudentSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'created_at', 'read']

class ClearanceDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceDocument
        fields = ['id', 'clearance_request', 'document', 'uploaded_at']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'student', 'department', 'file', 'uploaded_at']
        
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value

    def validate_new_password(self, value):
        # Add any additional password validations if needed
        return value