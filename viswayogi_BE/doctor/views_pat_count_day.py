from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Appointment,PatientProfile
from user_profile.models import UserProfile
from .serializers import AppointmentSerializer
from user_profile.decorators import authenticate_user_session
from django.db.models import F
from django.db.models import Count, Case, When, IntegerField, DateField
from django.db.models.functions import TruncDate


HEADER_PARAMS = {
    'access_token': openapi.Parameter('accesstoken', openapi.IN_HEADER, description="Local header param", type=openapi.TYPE_STRING),
}

class FetchPatCountView(APIView):
    @swagger_auto_schema(
        operation_description="To fetch the appointment queue.",
        manual_parameters=[HEADER_PARAMS['access_token']],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "auth_params": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Authentication-related parameters (optional)",
                    properties={
                        "user_id": openapi.Schema(type=openapi.TYPE_STRING, description="User ID"),
                        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING, description="Any other parameter"),
                    },
                ),
                "payload": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Appointment details",
                    properties={
                        "doctor_id": openapi.Schema(type=openapi.TYPE_STRING, description="doctor id")
                    },
                    required=["doctor_id"],
                ),
            },
            required=["auth_params", "payload"],
        ),
        responses={
            201: openapi.Response(
                "Appointment booked successfully",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "appointment_data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Serialized appointment data",
                            properties={
                                "appointment_id": openapi.Schema(type=openapi.TYPE_STRING, description="Appointment ID"),
                                "assignment_id": openapi.Schema(type=openapi.TYPE_STRING, description="Assignment ID"),
                                "blood_pressure": openapi.Schema(type=openapi.TYPE_STRING, description="Blood pressure"),
                                "weight": openapi.Schema(type=openapi.TYPE_STRING, description="Weight"),
                                "body_temp": openapi.Schema(type=openapi.TYPE_STRING, description="Body temperature"),
                                "apponitment_reason": openapi.Schema(type=openapi.TYPE_STRING, description="Health condition"),
                                "ready": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Ready status"),
                                "appointment_sch": openapi.Schema(type=openapi.FORMAT_DATETIME, description="Scheduled appointment time"),
                                "added_date": openapi.Schema(type=openapi.FORMAT_DATETIME, description="Creation date"),
                            },
                        ),
                    },
                ),
            ),
            400: "Validation errors",
        },
    )

    @authenticate_user_session
    def post(self, request):
        payload = request.data.get('payload', {})
        doctor_id = payload.get('doctor_id')
        

        if not all([doctor_id]):
            return Response(
                {"error": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Assuming PatientProfile and UserProfile are linked to patient_phone and doctor_id
            doctor = UserProfile.objects.get(user_id=doctor_id)
        except doctor.DoesNotExist:
            return Response(
                {"error": "Doctor with the given ID does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )


        daily_stats = (
            Appointment.objects.filter(user_id=doctor_id)  # Filter by doctor
            .annotate(registration_date=TruncDate("appointment_sch"))  # Extract date
            .values("registration_date")
            .annotate(
                total_patients=Count("appointment_id"),
                done_count=Count(Case(When(done=True, then=1), output_field=IntegerField())),
                not_done_count=Count(Case(When(done=False, then=1), output_field=IntegerField())),
            )
            .order_by("-registration_date")  # Latest first
        )



        

        return Response(
            {"message": "Appointment queue", "appointment_data": daily_stats},
            status=status.HTTP_201_CREATED,
        )
