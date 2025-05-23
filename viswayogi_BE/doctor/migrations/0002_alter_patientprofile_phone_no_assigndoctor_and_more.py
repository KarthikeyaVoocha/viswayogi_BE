# Generated by Django 4.2.6 on 2024-12-29 08:56

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_alter_userprofile_role'),
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprofile',
            name='phone_no',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.CreateModel(
            name='AssignDoctor',
            fields=[
                ('assignment_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phone_no', models.CharField(max_length=15, unique=True)),
                ('phone_code', models.CharField(default='91', max_length=10)),
                ('health_conditon', models.CharField(max_length=2000, null=True)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(default=datetime.datetime.now)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.patientprofile')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('appointment_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('blood_pressure', models.CharField(max_length=15, unique=True)),
                ('weight', models.CharField(max_length=15, unique=True)),
                ('body_temp', models.CharField(max_length=15, unique=True)),
                ('health_conditon', models.CharField(max_length=2000, null=True)),
                ('appointment_sch', models.DateTimeField(auto_now_add=True)),
                ('ready', models.BooleanField()),
                ('done', models.BooleanField(default=False)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(default=datetime.datetime.now)),
                ('assignment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.patientprofile')),
            ],
        ),
    ]
