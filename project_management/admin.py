from django.contrib import admin
from django.utils.html import format_html

from . import models
from .models import ProjectManagement
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from datetime import datetime
from .forms import ProjectManagementAdminForm



@admin.register(ProjectManagement)
class ProjectManagementAdmin(admin.ModelAdmin):
    list_display = ['project_id', 'project_name', 'image_preview', 'description_preview', 'modified_date_only', 'status',
                    'action_buttons']
    form = ProjectManagementAdminForm
    search_fields = ['project_name', 'description']
    readonly_fields = []
    exclude = ['modified_date']
    fields = ['project_name', 'featured_image', 'description', 'status']
    change_list_template = "admin/project_management/project_management_change_list.html"

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if 'modified_date' in fields:
            fields.remove('modified_date')
        return fields

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'modified_date' in form.base_fields:
            del form.base_fields['modified_date']
        # Increase the text area size for project_name field
        if 'project_name' in form.base_fields:
            form.base_fields['project_name'].widget.attrs.update({
                'dir': 'auto',
                'class': 'bilingual-field vLargeTextField',
                'style': 'width: 100%; min-width: 600px; height: 60px; padding: 10px; font-size: 14px; resize: horizontal;',
                'rows': 3,
                'cols': 80
            })
        return form

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Handle status filter - Fixed: Only filter if status is not empty and not 'all'
        status = request.GET.get('status')
        if status and status != '' and status != 'all':
            queryset = queryset.filter(status=status)

        # Handle search query - Fixed: Handle search from horizontal filter
        search_query = request.GET.get('q')  # Changed from default search to 'q'
        if search_query:
            queryset = queryset.filter(
                models.Q(project_name__icontains=search_query) |
                models.Q(description__icontains=search_query)
            )

        # Handle modified date filter
        modified_date = request.GET.get('modified_date')
        if modified_date:
            try:
                date = datetime.strptime(modified_date, '%Y-%m-%d')
                queryset = queryset.filter(modified_date__date=date)
            except ValueError:
                pass

        return queryset

    def modified_date_only(self, obj):
        """Display only the date part of modified_date"""
        if obj.modified_date:
            return obj.modified_date.strftime('%Y-%m-%d')
        return '-'

    modified_date_only.short_description = _('Modified Date')
    modified_date_only.admin_order_field = 'modified_date'  # Allow sorting by this field

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />',
                               obj.featured_image.url)
        return _("No Image")

    image_preview.short_description = _('Image')

    def description_preview(self, obj):
        from django.utils.html import strip_tags
        clean_description = strip_tags(obj.description)
        return clean_description[:100] + '...' if len(clean_description) > 100 else clean_description

    description_preview.short_description = _('Description')

    def action_buttons(self, obj):
        return format_html(
            '<a class="button action-button edit-button" href="{}" style="margin-right: 5px;">'
            '<i class="fas fa-edit"></i> {}</a>'
            '<a class="button action-button delete-button" href="{}" style="color: red;">'
            '<i class="fas fa-trash"></i> {}</a>',
            f'/admin/project_management/projectmanagement/{obj.pk}/change/',
            _('Edit'),
            f'/admin/project_management/projectmanagement/{obj.pk}/delete/',
            _('Delete')
        )

    action_buttons.short_description = _('Actions')

    class Media:
        css = {
            'all': (
                'https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap',
            )
        }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['project_name'].widget.attrs.update({
            'dir': 'auto',
            'class': 'bilingual-field'
        })
        form.base_fields['description'].widget.attrs.update({
            'dir': 'auto',
            'class': 'bilingual-field'
        })
        return form
