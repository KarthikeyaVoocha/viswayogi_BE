import uuid
from datetime import datetime
from django.db import models


class PatientProfileStatus(models.Model):
    status_id = models.CharField(primary_key=True,max_length=100)
    status_name = models.CharField(max_length=50)

    def __str__(self):
        return self.status_id


class PatientProfile(models.Model):
    patient_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, null=True)
    email_id = models.EmailField(max_length=100, unique=True, null=True)
    phone_no = models.CharField(max_length=15, null=False, unique=True)
    phone_code = models.CharField(default="91", max_length=10)
    address = models.CharField(max_length=200, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(default=datetime.now)
    status = models.ForeignKey(PatientProfileStatus, default="1", on_delete=models.CASCADE)

    def __str__(self):
        return self.patient_id