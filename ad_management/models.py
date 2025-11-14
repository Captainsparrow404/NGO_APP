from django.db import models

class Advertisement(models.Model):
    title = models.CharField(max_length=255, verbose_name='Ad Title', help_text='Enter advertisement title')
    featured_image = models.ImageField(upload_to='advertisements/', verbose_name='Featured Image', help_text='Upload advertisement image')
    third_party_link = models.URLField(blank=True, null=True, verbose_name='Third Party Link', help_text='Enter third party URL (optional)')
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active',
        verbose_name='Status'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'
        ordering = ['-created_at']

    def __str__(self):
        return self.title