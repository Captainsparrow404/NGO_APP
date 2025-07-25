# Generated by Django 5.2.4 on 2025-07-10 12:11

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='case_name',
            field=models.CharField(help_text='Enter case name (supports Arabic)', max_length=255, verbose_name='Case Name'),
        ),
        migrations.AlterField(
            model_name='case',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='Case description (supports Arabic)', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='case',
            name='featured_image',
            field=models.ImageField(help_text='Upload case image', upload_to='cases/', verbose_name='Featured Image'),
        ),
    ]
