from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import PatientProfile, AssignDoctor
from .serializers import AssignDoctorSerializer
from user_profile.decorators import authenticate_user_session

HEADER_PARAMS = {
    'access_token': openapi.Parameter('accesstoken', openapi.IN_HEADER, description="local header param", type=openapi.TYPE_STRING),
}

class AssignDoctorView(APIView):
    @swagger_auto_schema(
        operation_description="To assign a doctor to a patient.",
        manual_parameters=[HEADER_PARAMS['access_token']],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "auth_params": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Authentication-related parameters (optional)",
                    properties={
                        "user_id": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's User ID"),
                        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING, description="Any other parameter"),
                    },
                ),
                "payload": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Doctor assignment details",
                    properties={
                        "doctor_id": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's User ID"),
                        "patient_phone": openapi.Schema(type=openapi.TYPE_STRING, description="Patient's phone number"),
                        "health_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Health condition of the patient"),
                    },
                    required=["doctor_id", "patient_phone", "health_condition"],
                ),
            },
            required=["auth_params", "payload"],
        ),
        responses={
            201: openapi.Response(
                "Doctor assigned successfully",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "assignment_data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Serialized assignment data",
                            properties={
                                "assignment_id": openapi.Schema(type=openapi.TYPE_STRING, description="Assignment ID"),
                                "patient_id": openapi.Schema(type=openapi.TYPE_STRING, description="Patient ID"),
                                "doctor_id": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor ID"),
                                "health_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Health condition"),
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
        patient_phone = payload.get('patient_phone')
        health_condition = payload.get('health_condition')

        if not doctor_id or not patient_phone or not health_condition:
            return Response(
                {"error": "Doctor ID, patient phone number, and health condition are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            patient = PatientProfile.objects.get(phone_no=patient_phone)
        except PatientProfile.DoesNotExist:
            return Response(
                {"error": "Patient with the given phone number does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        assignment_data = {
            "patient_id": patient.patient_id,
            "user_id": doctor_id,
            "phone_no": patient_phone,
            "phone_code": patient.phone_code,
            "health_conditon": health_condition,
        }

        serializer = AssignDoctorSerializer(data=assignment_data)
        if serializer.is_valid():
            assignment = serializer.save()

            response_data = {
                "assignment_id": str(assignment.assignment_id),
                "patient_id": str(assignment.patient_id.patient_id),
                "doctor_id": str(assignment.user_id),
                "health_condition": assignment.health_conditon,
                "added_date": assignment.added_date,
            }

            return Response(
                {"message": "Doctor assigned successfully", "assignment_data": response_data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
