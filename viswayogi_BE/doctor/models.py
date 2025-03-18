import uuid
from datetime import datetime
from django.db import models
from user_profile.models import UserProfile


class PatientProfileStatus(models.Model):
    status_id = models.CharField(primary_key=True,max_length=100)
    status_name = models.CharField(max_length=50)

    def __str__(self):
        return self.status_id


class PatientProfile(models.Model):
    patient_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, null=True)
    email_id = models.EmailField(max_length=100, null=True)
    Sex = models.CharField(max_length=100, null=False)
    DOB = models.DateTimeField(default=datetime.now,null=False)
    Health_info = models.CharField(max_length=2000, null=False) 
    phone_no = models.CharField(max_length=15, null=False, unique=True)
    phone_code = models.CharField(default="91", max_length=10)
    address = models.CharField(max_length=200, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(default=datetime.now)
    status = models.ForeignKey(PatientProfileStatus, default="1", on_delete=models.CASCADE)

    def __str__(self):
        return self.patient_id
    

class Appointment(models.Model):
    appointment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    room_no = models.CharField(max_length=100, null=True)
    blood_pressure = models.CharField(max_length=15, null=False)
    weight = models.CharField(max_length=15, null=False)
    body_temp = models.CharField(max_length=15, null=False)
    apponitment_reason = models.CharField(max_length=2000, null=True)
    appointment_sch = models.DateTimeField(auto_now_add=True)
    prescription = models.TextField(null=True)
    diagnosis = models.TextField(null=True)
    ready = models.BooleanField()
    done = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.appointment_id