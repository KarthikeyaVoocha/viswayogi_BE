from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import PatientProfile
from user_profile.decorators import authenticate_user_session

HEADER_PARAMS = {
    'access_token': openapi.Parameter('accesstoken', openapi.IN_HEADER, description="local header param", type=openapi.TYPE_STRING),
}

class FetchPatientNameView(APIView):
    @swagger_auto_schema(
        operation_description="Fetch patient name.",
        manual_parameters=[HEADER_PARAMS['access_token']],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "auth_params": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Authentication-related parameters",
                    properties={
                        "user_id": openapi.Schema(type=openapi.TYPE_STRING, description="Authenticated user's ID"),
                        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token"),
                    },
                    required=["user_id", "refresh_token"],
                ),
                "payload": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="payload for fetching patient name",
                    properties={
                        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, description="Phone number")
                    },
                    required=["phone_number"]
                ),
            },
            required=["auth_params", "payload"],
        ),
        responses={
            200: openapi.Response(
                "Doctors fetched successfully",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "doctors": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            description="List of doctors",
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "user_id": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's User ID"),
                                    "full_name": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's full name"),
                                    "email": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's email"),
                                    "phone_no": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's phone number"),
                                },
                            ),
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
        phone_number = payload.get('phone_number')

        if not phone_number:
            return Response(
                {"error": "Phone number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            patient = PatientProfile.objects.get(phone_no=phone_number)
        except PatientProfile.DoesNotExist:
            return Response(
                {"error": "Patient with the given phone number does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        response_data = {
            "message": "Patient name retrieved successfully",
            "patient_full_name": patient.full_name,
        }

        return Response(response_data, status=status.HTTP_200_OK)