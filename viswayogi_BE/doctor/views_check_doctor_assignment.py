from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import AssignDoctor
from user_profile.decorators import authenticate_user_session

HEADER_PARAMS = {
    'access_token': openapi.Parameter('accesstoken', openapi.IN_HEADER, description="local header param", type=openapi.TYPE_STRING),
}

class CheckDoctorAssignmentView(APIView):
    @swagger_auto_schema(
        operation_description="To check if a doctor is assigned to a patient.",
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
                    description="Doctor-patient relationship check details",
                    properties={
                        "doctor_id": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's User ID"),
                        "patient_phone": openapi.Schema(type=openapi.TYPE_STRING, description="Patient's phone number"),
                    },
                    required=["doctor_id", "patient_phone"],
                ),
            },
            required=["auth_params", "payload"],
        ),
        responses={
            200: openapi.Response(
                "Check completed successfully",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "exists": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="True if the relationship exists, False otherwise"),
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

        if not doctor_id or not patient_phone:
            return Response(
                {"error": "Doctor ID and patient phone number are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        exists = AssignDoctor.objects.filter(user_id=doctor_id, phone_no=patient_phone).exists()

        return Response(
            {"exists": exists},
            status=status.HTTP_200_OK,
        )
