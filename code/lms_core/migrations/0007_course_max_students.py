# Generated by Django 5.1.4 on 2025-01-05 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_core', '0006_coursecontent_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='max_students',
            field=models.IntegerField(default=30, verbose_name='Jumlah Maksimal Siswa'),
        ),
    ]
