# Generated by Django 5.2.4 on 2025-07-14 11:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cases', '0002_alter_case_case_name_alter_case_description_and_more'),
        ('project_management', '0002_alter_projectmanagement_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderManagement',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_case_title', models.CharField(max_length=255, verbose_name='Project/Case Title')),
                ('donation_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Donation Amount')),
                ('currency', models.CharField(choices=[('SAR', 'Saudi Riyal (SAR)')], default='SAR', max_length=3, verbose_name='Currency')),
                ('sender_name', models.CharField(max_length=255, verbose_name="Sender's Name")),
                ('recipient_name', models.CharField(max_length=255, verbose_name="Recipient's Name")),
                ('phone', models.CharField(max_length=20, verbose_name='Phone')),
                ('gift_template', models.CharField(blank=True, max_length=255, null=True, verbose_name='Gift Template')),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20, verbose_name='Payment Status')),
                ('payment_information', models.TextField(blank=True, null=True, verbose_name='Payment Information')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='cases.case', verbose_name='Case')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='project_management.projectmanagement', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-created_date'],
            },
        ),
    ]
