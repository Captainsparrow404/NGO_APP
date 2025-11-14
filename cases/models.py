from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

class Case(models.Model):
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
    ]

    case_id = models.AutoField(primary_key=True)
    case_name = models.CharField(
        max_length=255,
        verbose_name=_("Case Name"),
        help_text=_("Enter case name (supports Arabic)")
    )
    featured_image = models.ImageField(
        upload_to='cases/',
        verbose_name=_("Featured Image"),
        help_text=_("Upload case image")
    )
    description = RichTextUploadingField(
        verbose_name=_("Description"),
        help_text=_("Project description (supports Arabic)"),
        blank=True,  # Make field optional
        null=True    # Allow NULL in database
    )
    start_date = models.DateField(
        default=timezone.now,
        verbose_name=_("Start Date"),
        help_text=_("Automatically set when case is created")
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("End Date"),
        help_text=_("Set the end date for this case")
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
        from order_management.models import OrderManagement  # Avoid circular import
        total = OrderManagement.objects.filter(
            case=self,
            payment_status='completed'
        ).aggregate(total=models.Sum('donation_amount'))['total']
        return float(total) if total else 0.0

    class Meta:
        verbose_name = _('Case')
        verbose_name_plural = _('Cases')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.case_name} (ID: {self.case_id})"