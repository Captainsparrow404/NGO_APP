from rest_framework import serializers
from .models import ProjectManagement

class ProjectManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManagement
        fields = '__all__'