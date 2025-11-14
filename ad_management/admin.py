from django.contrib import admin
from .models import Advertisement
from django.utils.html import format_html

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured_image_display', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def featured_image_display(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.featured_image.url)
        return "-"
    featured_image_display.short_description = 'Featured Image'

    def save_model(self, request, obj, form, change):
        if obj.status == 'active':
            # Deactivate all other advertisements
            Advertisement.objects.exclude(pk=obj.pk).update(status='inactive')
        super().save_model(request, obj, form, change)