# Generated by Django 4.2.6 on 2025-03-20 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0008_patientprofile_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='room_no',
        ),
        migrations.AddField(
            model_name='appointment',
            name='room_num',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
