from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CaseViewSet

router = DefaultRouter()
router.register(r'', CaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]