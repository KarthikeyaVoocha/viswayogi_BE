from django.urls import path
from .views_register_patient import PatientRegisterView
from .views_assign_doctor import AssignDoctorView
from .views_fetch_doctors import FetchDoctorsView
from .views_book_appointment import BookAppointmentView
from .views_check_doctor_assignment import CheckDoctorAssignmentView

urlpatterns = [
    path('patient_register/', PatientRegisterView.as_view(), name='patient_register'),
    path('assign_doctor/', AssignDoctorView.as_view(), name='assign_doctor'),
    path('fetch_doctors/', FetchDoctorsView.as_view(), name='fetch_doctors'),
    path('book_appointment/', BookAppointmentView.as_view(), name='book_appointment'),
    path('check_doctor_assignment/', CheckDoctorAssignmentView.as_view(), name='check_doctor_assignment'),

]