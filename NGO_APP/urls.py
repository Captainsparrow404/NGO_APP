from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken import views
from NGO_APP.admin import admin_site

schema_view = get_schema_view(
    openapi.Info(
        title="NGO APP API",
        default_version='v1',
        description="""
        API documentation for NGO APP.

        Donations API Endpoints:
        - POST /api/orders/donations/ - Create a new donation
        - GET /api/orders/donations/project_donations/?project_id={id} - Get donations for a project
        - GET /api/orders/donations/case_donations/?case_id={id} - Get donations for a case

        To authorize, use Token authentication with format: 'Token <your-token>'
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@ngoapp.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,  # Change this to False to require authentication
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    path('admin/', admin_site.urls),
    path('api/projects/', include('project_management.urls')),
    path('api/cases/', include('cases.urls')),
    path('api/orders/', include('order_management.urls')),
    path('ckeditor/upload/', include('ckeditor_uploader.urls')),

    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Authentication endpoints
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
