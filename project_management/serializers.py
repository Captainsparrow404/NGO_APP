from rest_framework import serializers
from .models import ProjectManagement

class ProjectManagementSerializer(serializers.ModelSerializer):
    modified_date = serializers.SerializerMethodField()

    class Meta:
        model = ProjectManagement
        fields = ['project_id', 'project_name', 'featured_image', 'description', 'modified_date', 'status']

    def get_modified_date(self, obj):
        return obj.modified_date.strftime('%Y-%m-%d')