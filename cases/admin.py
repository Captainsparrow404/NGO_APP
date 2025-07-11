from django.contrib import admin
from django.utils.html import format_html
from .models import Case
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from datetime import datetime
from django.db import models
from .forms import CaseAdminForm


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    form = CaseAdminForm
    list_display = ['case_id', 'case_name', 'image_preview', 'description_preview', 'modified_date_only', 'status',
                    'action_buttons']
    search_fields = ['case_name', 'description']
    readonly_fields = []
    exclude = ['modified_date']
    fields = ['case_name', 'featured_image', 'description', 'status']
    change_list_template = "admin/cases/case_change_list.html"

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if 'modified_date' in fields:
            fields.remove('modified_date')
        return fields

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Handle status filter - Fixed logic
        status = request.GET.get('status')
        if status and status.strip() != '' and status != 'all':  # Only filter if status is not empty or 'all'
            queryset = queryset.filter(status=status)

        # Handle search query - Let Django handle the built-in search
        # Remove custom search handling to avoid conflicts

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

    def changelist_view(self, request, extra_context=None):
        """Override changelist view to pass additional context"""
        extra_context = extra_context or {}
        # Add current filter values to context
        extra_context.update({
            'current_status': request.GET.get('status', ''),
            'current_search': request.GET.get('q', ''),
            'current_date': request.GET.get('modified_date', ''),
        })
        return super().changelist_view(request, extra_context=extra_context)

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
            '<a class="button" href="{}" style="margin-right: 5px;">{}</a>'
            '<a class="button" href="{}" style="color: red;">{}</a>',
            f'/admin/cases/case/{obj.pk}/change/',
            _('Edit'),
            f'/admin/cases/case/{obj.pk}/delete/',
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
        if 'modified_date' in form.base_fields:
            del form.base_fields['modified_date']
        form.base_fields['case_name'].widget.attrs.update({
            'dir': 'auto',
            'class': 'bilingual-field'
        })
        form.base_fields['description'].widget.attrs.update({
            'dir': 'auto',
            'class': 'bilingual-field'
        })
        return form
