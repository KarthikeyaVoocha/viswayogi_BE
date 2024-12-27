from django.urls import path
from .views_register_patient import PatientRegisterView

urlpatterns = [
    path('patient_register/', PatientRegisterView.as_view(), name='patient_register')
]