from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.shortcuts import render, get_object_or_404
from .models import Case
from .forms import CaseAdminForm
from order_management.models import OrderManagement

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    form = CaseAdminForm
    list_display = [
        'case_id', 'case_name', 'description_preview', 'formatted_start_date', 'formatted_end_date',
        'formatted_goal_amount', 'status', 'total_donation', 'action_buttons'
    ]
    list_filter = []
    search_fields = ['case_name', 'description']
    readonly_fields = ['start_date']

    def description_preview(self, obj):
        from django.utils.html import strip_tags
        clean_description = strip_tags(obj.description)
        return clean_description[:100] + '...' if len(clean_description) > 100 else clean_description

    description_preview.short_description = _('Description')

    def formatted_start_date(self, obj):
        return obj.start_date.strftime('%Y-%m-%d') if obj.start_date else ''

    formatted_start_date.short_description = _('Start Date')

    def formatted_end_date(self, obj):
        return obj.end_date.strftime('%Y-%m-%d') if obj.end_date else ''

    formatted_end_date.short_description = _('End Date')

    def formatted_goal_amount(self, obj):
        return f'{obj.goal_amount:,.2f} SAR' if obj.goal_amount else ''

    formatted_goal_amount.short_description = _('Goal Amount')

    def total_donation(self, obj):
        return obj.get_total_donations()
    total_donation.short_description = _('Total Donation (SAR)')

    def action_buttons(self, obj):
        edit_url = f'/admin/cases/case/{obj.pk}/change/'
        delete_url = f'/admin/cases/case/{obj.pk}/delete/'
        details_url = self.get_view_details_url(obj)
        return format_html(
            '<a class="button" href="{}" style="margin-right: 5px;">{}</a>'
            '<a class="button" href="{}" style="color: red; margin-right: 5px;">{}</a>'
            '<a class="button" href="{}" style="color: green;">{}</a>',
            edit_url, _('Edit'),
            delete_url, _('Delete'),
            details_url, _('View Details')
        )
    action_buttons.short_description = _('Actions')

    def get_view_details_url(self, obj):
        return f"/admin/cases/case/{obj.pk}/donation_details/"

    class Media:
        css = {
            'all': (
                'https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap',
            )
        }

    def get_fields(self, request, obj=None):
        fields = ['case_name', 'featured_image', 'description', 'end_date', 'goal_amount', 'status']
        if obj:  # If editing an existing object
            fields.insert(3, 'start_date')
        return fields

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:case_id>/donation_details/',
                self.admin_site.admin_view(self.donation_details_view),
                name='case_donation_details',
            ),
        ]
        return custom_urls + urls

    def donation_details_view(self, request, case_id):
        case = get_object_or_404(Case, pk=case_id)
        donations = OrderManagement.objects.filter(case=case, payment_status='completed')
        # Filtering by donated amount
        amount = request.GET.get('amount')
        if amount:
            donations = donations.filter(donation_amount=amount)
        context = dict(
            self.admin_site.each_context(request),
            case=case,
            donations=donations,
            request=request,
        )
        return render(request, 'admin/cases/donation_details.html', context)