from django.urls import path
from .views_register_patient import PatientRegisterView
from .views_fetch_doctors import FetchDoctorsView
from .views_book_appointment import BookAppointmentView
from .views_fetch_patient_name import FetchPatientNameView

urlpatterns = [
    path('patient_register/', PatientRegisterView.as_view(), name='patient_register'),
    path('fetch_doctors/', FetchDoctorsView.as_view(), name='fetch_doctors'),
    path('book_appointment/', BookAppointmentView.as_view(), name='book_appointment'),
    path('fetch_patient_name/', FetchPatientNameView.as_view(), name='fetch_patient_name')
]