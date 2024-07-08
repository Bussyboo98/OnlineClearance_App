from django.db import models
from django.contrib.auth.models import AbstractUser

class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, related_name='departments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ClearanceStatus(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status

class Student(AbstractUser):
    MALE = 'Male'
    FEMALE = 'Female'
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    
    matric_number = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    department = models.ForeignKey(Department, related_name='students', on_delete=models.CASCADE, null=True)
    clearance_status = models.ForeignKey(ClearanceStatus, related_name='students', on_delete=models.SET_NULL, null=True, blank=True)
    is_cleared = models.BooleanField(default=False)

    def __str__(self):
        return self.matric_number



class Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='documents')
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.department.name} - {self.file.name}"