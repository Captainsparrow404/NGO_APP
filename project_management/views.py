from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ProjectManagement
from .serializers import ProjectManagementSerializer
from drf_yasg.utils import swagger_auto_schema

class ProjectManagementViewSet(viewsets.ModelViewSet):
    queryset = ProjectManagement.objects.all()
    serializer_class = ProjectManagementSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all projects",
        responses={200: ProjectManagementSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new project",
        request_body=ProjectManagementSerializer,
        responses={201: ProjectManagementSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)