from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Appointment, AssignDoctor
from .serializers import AppointmentSerializer
from user_profile.decorators import authenticate_user_session

HEADER_PARAMS = {
    'access_token': openapi.Parameter('accesstoken', openapi.IN_HEADER, description="Local header param", type=openapi.TYPE_STRING),
}

class BookAppointmentView(APIView):
    @swagger_auto_schema(
        operation_description="To book an appointment for a patient.",
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
                        "assignment_id": openapi.Schema(type=openapi.TYPE_STRING, description="Assignment ID"),
                        "blood_pressure": openapi.Schema(type=openapi.TYPE_STRING, description="Blood pressure reading"),
                        "weight": openapi.Schema(type=openapi.TYPE_STRING, description="Weight of the patient"),
                        "body_temp": openapi.Schema(type=openapi.TYPE_STRING, description="Body temperature"),
                        "health_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Health condition details"),
                        "ready": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is the appointment ready?"),
                        "appointment_sch": openapi.Schema(type=openapi.FORMAT_DATETIME, description="Scheduled appointment time"),
                    },
                    required=["assignment_id", "blood_pressure", "weight", "body_temp", "health_condition", "ready", "appointment_sch"],
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
                                "health_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Health condition"),
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
        assignment_id = payload.get('assignment_id')
        blood_pressure = payload.get('blood_pressure')
        weight = payload.get('weight')
        body_temp = payload.get('body_temp')
        health_condition = payload.get('health_condition')
        ready = payload.get('ready')
        appointment_sch = payload.get('appointment_sch')

        if not all([assignment_id, blood_pressure, weight, body_temp, health_condition, ready is not None, appointment_sch]):
            return Response(
                {"error": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            assignment = AssignDoctor.objects.get(assignment_id=assignment_id)
        except AssignDoctor.DoesNotExist:
            return Response(
                {"error": "Assignment with the given ID does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment_data = {
            "assignment_id": assignment_id,
            "blood_pressure": blood_pressure,
            "weight": weight,
            "body_temp": body_temp,
            "health_conditon": health_condition,
            "ready": ready,
            "appointment_sch": appointment_sch,
        }

        serializer = AppointmentSerializer(data=appointment_data)
        if serializer.is_valid():
            appointment = serializer.save()

            response_data = {
                "appointment_id": str(appointment.appointment_id),
                "assignment_id": str(appointment.assignment_id.assignment_id),
                "blood_pressure": appointment.blood_pressure,
                "weight": appointment.weight,
                "body_temp": appointment.body_temp,
                "health_condition": appointment.health_conditon,
                "ready": appointment.ready,
                "appointment_sch": appointment.appointment_sch,
                "added_date": appointment.added_date,
            }

            return Response(
                {"message": "Appointment booked successfully", "appointment_data": response_data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)