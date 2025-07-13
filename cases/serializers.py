from rest_framework import serializers
from .models import Case

class CaseSerializer(serializers.ModelSerializer):
    modified_date = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = ['case_id', 'case_name', 'featured_image', 'description', 'modified_date', 'status']

    def get_modified_date(self, obj):
        return obj.modified_date.strftime('%Y-%m-%d')