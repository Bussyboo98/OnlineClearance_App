from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import  *

urlpatterns = [
      path('login/', CustomAuthToken.as_view(), name='api_login'),
     path('faculties/', FacultyListView.as_view(), name='faculty-list'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('clearance-statuses/', ClearanceStatusListView.as_view(), name='clearance-status-list'),
    path('students/', StudentCreateView.as_view(), name='student-create'),
    path('students/all/', StudentListView.as_view(), name='student-list'),
    path('documents/', DocumentListView.as_view(), name='document-list'),
   path('upload/', FileUploadView.as_view(), name='file-upload'),
     path('admin/students/', AdminStudentCreateView.as_view(), name='admin-student-create'), 
    path('students/<int:student_id>/clear/', ClearStudentView.as_view(), name='clear-student'),
    path('user/', UserDetails.as_view(), name='user_details'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    

]