from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _


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
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-modified_date']

    def __str__(self):
        return f"{self.project_name} (ID: {self.project_id})"