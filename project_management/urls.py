from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProjectManagementViewSet

router = DefaultRouter()
router.register(r'', ProjectManagementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]