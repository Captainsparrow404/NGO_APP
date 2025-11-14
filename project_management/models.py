from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

class ProjectManagement(models.Model):
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
    ]

    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(
        max_length=255,
        verbose_name=_("Project Name"),
        help_text=_("Enter project name (supports Arabic)")
    )
    featured_image = models.ImageField(
        upload_to='projects/',
        verbose_name=_("Featured Image"),
        help_text=_("Upload project image")
    )
    description = RichTextUploadingField(
        verbose_name=_("Description"),
        help_text=_("Project description (supports Arabic)")
    )
    start_date = models.DateField(
        default=timezone.now,
        verbose_name=_("Start Date"),
        help_text=_("Automatically set when project is created")
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("End Date"),
        help_text=_("Set the end date for this project")
    )
    goal_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Goal Amount (SAR)"),
        help_text=_("Set the goal amount in Saudi Riyal"),
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name=_("Status")
    )

    def get_total_donations(self):
        """Calculate total donations for this project"""
        from order_management.models import OrderManagement  # Import here to avoid circular imports

        total = OrderManagement.objects.filter(
            project=self,
            payment_status='completed'
        ).aggregate(
            total=models.Sum('donation_amount')
        )['total']
        return float(total) if total else 0.0

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.project_name} (ID: {self.project_id})"