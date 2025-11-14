from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrderManagementViewSet

router = DefaultRouter()
router.register(r'', OrderManagementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]