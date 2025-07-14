from rest_framework import serializers
from .models import OrderManagement

class OrderManagementSerializer(serializers.ModelSerializer):
    modified_date = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = OrderManagement
        fields = ['order_id', 'project', 'case', 'project_case_title',
                 'donation_amount', 'currency', 'sender_name', 'recipient_name',
                 'phone', 'gift_template', 'payment_status', 'payment_information',
                 'created_date', 'modified_date']

    def get_modified_date(self, obj):
        return obj.modified_date.strftime('%Y-%m-%d')

    def get_created_date(self, obj):
        return obj.created_date.strftime('%Y-%m-%d')