from django.urls import path
from .views_register_patient import PatientRegisterView
from .views_fetch_doctors import FetchDoctorsView
from .views_book_appointment import BookAppointmentView
from .views_fetch_patient_name import FetchPatientNameView
from .views_fetch_queue import FetchQueueView
from .views_update_queue import UpdateQueueView

urlpatterns = [
    path('patient_register/', PatientRegisterView.as_view(), name='patient_register'),
    path('fetch_doctors/', FetchDoctorsView.as_view(), name='fetch_doctors'),
    path('book_appointment/', BookAppointmentView.as_view(), name='book_appointment'),
    path('fetch_patient_name/', FetchPatientNameView.as_view(), name='fetch_patient_name'),
    path('fetch_queue/', FetchQueueView.as_view(), name='fetch_queue'),
    path('update_queue/', UpdateQueueView.as_view(), name='update_queue'),


]