from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from .models import Appointment
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import AppointmentSerializer
from user_profile.decorators import authenticate_user_session

HEADER_PARAMS = {
    'access_token': openapi.Parameter('accesstoken', openapi.IN_HEADER, description="local header param", type=openapi.IN_HEADER),
}

class UpdatePresView(APIView):
    """
    Updates an appointment and broadcasts the updated queue.
    """
    @swagger_auto_schema(
        operation_description="To update an appointment for a patient.",
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
                        "appointment_id": openapi.Schema(type=openapi.TYPE_STRING, description="Appointment ID"),
                        "presecription": openapi.Schema(type=openapi.TYPE_STRING, description="Is the appointment ready?"),
                    },
                    required=["assignment_id", "presecription"],
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
        appointment_id = payload.get('appointment_id')
        presecription = payload.get('presecription')
        try:
            appointment = Appointment.objects.get(appointment_id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentSerializer(appointment, data={"presecription": presecription}, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Appointment updated", "appointment": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
