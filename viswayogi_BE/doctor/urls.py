from django.urls import path
from .views_register_patient import PatientRegisterView
from .views_assign_doctor import AssignDoctorView
from .views_fetch_doctors import FetchDoctorsView

urlpatterns = [
    path('patient_register/', PatientRegisterView.as_view(), name='patient_register'),
    path('assign_doctor/', AssignDoctorView.as_view(), name='assign_doctor'),
    path('fetch_doctors/', FetchDoctorsView.as_view(), name='fetch_doctors')

]