from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Case
from .serializers import CaseSerializer
from drf_yasg.utils import swagger_auto_schema

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all cases",
        responses={200: CaseSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new case",
        request_body=CaseSerializer,
        responses={201: CaseSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)