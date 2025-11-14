from rest_framework import serializers
from .models import Case
from django.utils.html import strip_tags
import html
from order_management.models import OrderManagement
from django.db.models import Sum

class CaseSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(format='%Y-%m-%d')
    end_date = serializers.DateField(format='%Y-%m-%d', required=False)
    goal_amount = serializers.DecimalField(max_digits=10, decimal_places=3, required=False)
    description = serializers.SerializerMethodField()
    total_donation = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = ['case_id', 'case_name', 'featured_image', 'description',
                 'start_date', 'end_date', 'goal_amount', 'total_donation', 'status']

    def get_description(self, obj):
        # Strip HTML tags and unescape HTML entities
        clean_description = strip_tags(obj.description)
        clean_description = html.unescape(clean_description)
        # Remove extra whitespace
        return ' '.join(clean_description.split())

    def get_total_donation(self, obj):
        """Calculate total donations for this case"""
        total = OrderManagement.objects.filter(
            case=obj,
            payment_status='completed'
        ).aggregate(
            total=Sum('donation_amount')
        )['total']
        return float(total) if total else 0.0