from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone
from django.utils.html import format_html
from django.urls import path
from django.template.response import TemplateResponse
from .models import OrderManagement
from project_management.models import ProjectManagement
from cases.models import Case
from django.utils.translation import gettext_lazy as _

@admin.register(OrderManagement)
class OrderManagementAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'project_case_title', 'donation_amount', 'sender_name', 'payment_status', 'created_date']
    list_filter = []
    search_fields = ['sender_name', 'recipient_name', 'project__project_name', 'case__case_name']

    def has_add_permission(self, request):
        return False  # This removes the "Add" button

    def has_delete_permission(self, request, obj=None):
        return False  # Optional: This removes the "Delete" action

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']  # Remove bulk delete action
        return actions

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('donation-summary/', self.donation_summary_view, name='order_management_donation_summary'),
        ]
        return custom_urls + urls

    def donation_summary_view(self, request):
        # Get project donations summary
        projects = ProjectManagement.objects.all()
        project_donations = []

        for project in projects:
            donations = OrderManagement.objects.filter(
                project=project,
                payment_status='completed'
            )

            if donations.exists():
                total = donations.aggregate(total=Sum('donation_amount'))
                unique_donors = donations.values_list('sender_name', flat=True).distinct()
                last_donation = donations.order_by('-created_date').first()

                project_donations.append({
                    'id': project.project_id,
                    'title': project.project_name,
                    'total_donation': total['total'] or 0,
                    'donor_count': len(unique_donors),
                    'last_donation': last_donation.created_date.date() if last_donation else None,  # Only date
                    'type': 'Project'
                })

        # Get case donations summary
        cases = Case.objects.all()
        case_donations = []

        for case in cases:
            donations = OrderManagement.objects.filter(
                case=case,
                payment_status='completed'
            )

            if donations.exists():
                total = donations.aggregate(total=Sum('donation_amount'))
                unique_donors = donations.values_list('sender_name', flat=True).distinct()
                last_donation = donations.order_by('-created_date').first()

                case_donations.append({
                    'id': case.case_id,
                    'title': case.case_name,
                    'total_donation': total['total'] or 0,
                    'donor_count': len(unique_donors),
                    'last_donation': last_donation.created_date.date() if last_donation else None,  # Only date
                    'type': 'Case'
                })

        context = {
            **self.admin_site.each_context(request),
            'title': 'Donation Summary',
            'project_donations': project_donations,
            'case_donations': case_donations,
            'current_date': timezone.now().date(),  # Only date
            'current_user': request.user.username,
            'has_permission': True,
        }

        return TemplateResponse(request, 'admin/order_management/donation_summary.html', context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_donation_summary'] = True
        return super().changelist_view(request, extra_context=extra_context)