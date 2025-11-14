from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from order_management.models import OrderManagement
from order_management.admin import OrderManagementAdmin

# Unregister the default Group and User admin
admin.site.unregister(Group)
admin.site.unregister(User)


# Create custom admin site class
class CustomAdminSite(admin.AdminSite):
    site_header = 'NGO APP Administration'
    site_title = 'NGO APP Admin'
    index_title = 'NGO APP Administration'

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_list = [
            app for app in app_list
            if app['app_label'] not in ['auth', 'authtoken']
        ]
        return app_list


# Create a new admin site instance
admin_site = CustomAdminSite(name='customadmin')

# Register your models with the custom admin site
from project_management.models import ProjectManagement
from project_management.admin import ProjectManagementAdmin
from cases.models import Case
from cases.admin import CaseAdmin

# Register models with custom admin
admin_site.register(ProjectManagement, ProjectManagementAdmin)
admin_site.register(Case, CaseAdmin)
admin_site.register(OrderManagement, OrderManagementAdmin)

# If you still need User and Group management, but in a different location:
# Create a new app section for user management
class UserManagementAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')


admin_site.register(User, UserManagementAdmin)
admin_site.register(Group, GroupAdmin)
