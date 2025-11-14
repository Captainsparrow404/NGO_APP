from rest_framework import serializers
from django.db.models import Sum, Count as DbCount  # Renamed to avoid conflict
from .models import OrderManagement
from project_management.models import ProjectManagement
from cases.models import Case

class OrderManagementSerializer(serializers.ModelSerializer):
    total_donations = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()
    case_name = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderManagement
        fields = [
            'order_id', 
            'project', 
            'case', 
            'project_case_title',
            'project_name',
            'case_name',
            'donation_amount', 
            'currency', 
            'sender_name', 
            'recipient_name',
            'phone', 
            'payment_status', 
            'created_date',
            'total_donations'
        ]
        read_only_fields = ['order_id', 'project_case_title', 'total_donations', 'project_name', 'case_name']

    def get_total_donations(self, obj):
        try:
            if obj.project:
                total = OrderManagement.objects.filter(
                    project=obj.project,
                    payment_status='completed'
                ).aggregate(
                    total=Sum('donation_amount'),
                    donor_count=DbCount('sender_name', distinct=True)
                )
                return {
                    'amount': float(total['total'] or 0),
                    'currency': 'SAR',
                    'donor_count': total['donor_count'],
                    'project_id': obj.project.pk
                }
            elif obj.case:
                total = OrderManagement.objects.filter(
                    case=obj.case,
                    payment_status='completed'
                ).aggregate(
                    total=Sum('donation_amount'),
                    donor_count=DbCount('sender_name', distinct=True)
                )
                return {
                    'amount': float(total['total'] or 0),
                    'currency': 'SAR',
                    'donor_count': total['donor_count'],
                    'case_id': obj.case.pk
                }
        except Exception as e:
            return {
                'amount': 0,
                'currency': 'SAR',
                'donor_count': 0,
                'error': str(e)
            }
        return None

    def get_project_name(self, obj):
        try:
            return obj.project.project_name if obj.project else None
        except Exception:
            return None

    def get_case_name(self, obj):
        try:
            return obj.case.case_name if obj.case else None
        except Exception:
            return None