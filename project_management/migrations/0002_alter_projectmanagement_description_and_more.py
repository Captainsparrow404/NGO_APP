# Generated by Django 5.2.4 on 2025-07-10 12:11

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmanagement',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='Project description (supports Arabic)', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='projectmanagement',
            name='featured_image',
            field=models.ImageField(help_text='Upload project image', upload_to='projects/', verbose_name='Featured Image'),
        ),
        migrations.AlterField(
            model_name='projectmanagement',
            name='project_name',
            field=models.CharField(help_text='Enter project name (supports Arabic)', max_length=255, verbose_name='Project Name'),
        ),
    ]
