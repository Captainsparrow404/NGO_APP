from rest_framework import serializers
from .models import Advertisement

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'featured_image', 'third_party_link', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']