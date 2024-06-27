from rest_framework import generics, permissions
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from rest_framework import status



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


class FacultyListView(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartmentListView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClearanceStatusListView(generics.ListCreateAPIView):
    queryset = ClearanceStatus.objects.all()
    serializer_class = ClearanceStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartmentClearanceCreateView(generics.CreateAPIView):
    queryset = DepartmentClearance.objects.all()
    serializer_class = DepartmentClearanceSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartmentClearanceListView(generics.ListAPIView):
    queryset = DepartmentClearance.objects.all()
    serializer_class = DepartmentClearanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class StudentDepartmentClearanceListView(generics.ListAPIView):
    serializer_class = DepartmentClearanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return DepartmentClearance.objects.filter(student_id=student_id)

class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClearanceDocumentCreateView(generics.CreateAPIView):
    queryset = ClearanceDocument.objects.all()
    serializer_class = ClearanceDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClearanceDocumentListView(generics.ListAPIView):
    queryset = ClearanceDocument.objects.all()
    serializer_class = ClearanceDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]


class AdminStudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAdminUser]

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_serializer = DocumentSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentListView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        student_id = request.data.get('student')
        department_id = request.data.get('department')
        student = Student.objects.get(id=student_id)
        department = Department.objects.get(id=department_id)
        
        documents = []
        for file in files:
            document = Document(student=student, department=department, file=file)
            documents.append(document)

        Document.objects.bulk_create(documents)

        return Response(status=status.HTTP_201_CREATED)


class DocumentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class ClearStudentView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            student.is_cleared = True
            student.save()
            return Response({"message": "Student cleared successfully."}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(username=request.user.username)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)