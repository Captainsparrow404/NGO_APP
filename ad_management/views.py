from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Advertisement
from .serializers import AdvertisementSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

token_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description='Token authentication. Example: "Token your-token-here"',
    type=openapi.TYPE_STRING,
    required=True
)

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all advertisements",
        manual_parameters=[token_param],
        responses={200: AdvertisementSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new advertisement",
        manual_parameters=[token_param],
        request_body=AdvertisementSerializer,
        responses={201: AdvertisementSerializer()}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update an advertisement",
        manual_parameters=[token_param],
        request_body=AdvertisementSerializer,
        responses={200: AdvertisementSerializer()}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)