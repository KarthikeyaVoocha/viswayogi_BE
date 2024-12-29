from rest_framework import serializers
from .models import *

class PatientProfileStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfileStatus
        fields = '__all__'

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'

class AssignDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignDoctor
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'