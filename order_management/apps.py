from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class OrderManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order_management'
    verbose_name = _('Donations')  # This changes the app name in admin