from django.apps import AppConfig

class AdManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ad_management'
    verbose_name = 'Ad Management'  # This will be the name shown in admin