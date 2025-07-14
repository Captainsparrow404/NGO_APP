from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import OrderManagement
from .forms import OrderManagementAdminForm

@admin.register(OrderManagement)
class OrderManagementAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'project_case_title', 'donation_amount', 'currency',
                    'sender_name', 'recipient_name', 'payment_status', 'created_date_display']

    search_fields = ['order_id', 'project_case_title', 'sender_name', 'recipient_name']
    readonly_fields = ['created_date', 'modified_date']
    form = OrderManagementAdminForm

    fieldsets = (
        (_('Order Information'), {
            'fields': ('project', 'case', 'project_case_title', 'donation_amount', 'currency')
        }),
        (_('Customer Information'), {
            'fields': ('sender_name', 'recipient_name', 'phone', 'gift_template')
        }),
        (_('Payment Details'), {
            'fields': ('payment_status', 'payment_information')
        }),
        (_('System Information'), {
            'fields': ('created_date', 'modified_date'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        payment_status = request.GET.get('payment_status')
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        return queryset

    def created_date_display(self, obj):
        return obj.created_date.strftime('%Y-%m-%d %H:%M')
    created_date_display.short_description = _('Created Date')
    created_date_display.admin_order_field = 'created_date'

    class Media:
        css = {
            'all': (
                'https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
            )
        }