# Generated by Django 5.1.4 on 2025-01-05 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_core', '0004_remove_coursecontent_video_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='Disetujui'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='coursecontent',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
