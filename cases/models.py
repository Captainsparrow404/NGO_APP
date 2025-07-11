from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _


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
        help_text=_("Case description (supports Arabic)")
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Modified Date")
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name=_("Status")
    )

    class Meta:
        verbose_name = _('Case')
        verbose_name_plural = _('Cases')
        ordering = ['-modified_date']

    def __str__(self):
        return f"{self.case_name} (ID: {self.case_id})"