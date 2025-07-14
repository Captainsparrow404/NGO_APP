from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import OrderManagement
from .serializers import OrderManagementSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

token_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description='Token authentication. Example: "Token your-token-here"',
    type=openapi.TYPE_STRING,
    required=True
)

class OrderManagementViewSet(viewsets.ModelViewSet):
    queryset = OrderManagement.objects.all()
    serializer_class = OrderManagementSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all orders",
        manual_parameters=[token_param],
        responses={200: OrderManagementSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new order",
        manual_parameters=[token_param],
        request_body=OrderManagementSerializer,
        responses={201: OrderManagementSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)