from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Case
from .serializers import CaseSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

token_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description='Token authentication. Example: "Token your-token-here"',
    type=openapi.TYPE_STRING,
    required=True
)

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all cases",
        manual_parameters=[token_param],
        responses={200: CaseSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new case",
        manual_parameters=[token_param],
        request_body=CaseSerializer,
        responses={201: CaseSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)