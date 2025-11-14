from django.db import models
from django.utils.translation import gettext_lazy as _
from project_management.models import ProjectManagement
from cases.models import Case


class OrderManagement(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    ]

    CURRENCY_CHOICES = [
        ('SAR', _('Saudi Riyal (SAR)')),
    ]

    order_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        ProjectManagement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Project"),
        related_name='orders'
    )
    case = models.ForeignKey(
        Case,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Case"),
        related_name='orders'
    )
    project_case_title = models.CharField(
        max_length=255,
        verbose_name=_("Project/Case Title")
    )
    donation_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Goal Amount (SAR)"),
        help_text=_("Set the goal amount in Saudi Riyal"),
        null=True,
        blank=True
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='SAR',
        verbose_name=_("Currency")
    )
    sender_name = models.CharField(
        max_length=255,
        verbose_name=_("Sender's Name")
    )
    recipient_name = models.CharField(
        max_length=255,
        verbose_name=_("Recipient's Name")
    )
    phone = models.CharField(
        max_length=20,
        verbose_name=_("Phone")
    )
    gift_template = models.CharField(
        max_length=255,
        verbose_name=_("Gift Template"),
        blank=True,
        null=True
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name=_("Payment Status")
    )
    payment_information = models.TextField(
        verbose_name=_("Payment Information"),
        blank=True,
        null=True
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created Date")
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Modified Date")
    )

    class Meta:
        verbose_name = _('Donation')
        verbose_name_plural = _('Donations')
        ordering = ['-created_date']

    def __str__(self):
        return f"Donation #{self.order_id} - {self.project_case_title}"

    def save(self, *args, **kwargs):
        if self.project:
            self.project_case_title = self.project.project_name
        elif self.case:
            self.project_case_title = self.case.case_name
        super().save(*args, **kwargs)