# Generated by Django 4.2.6 on 2024-12-29 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(default='demo', max_length=50),
            preserve_default=False,
        ),
    ]